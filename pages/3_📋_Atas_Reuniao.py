"""
Módulo de Atas de Reunião
Gerenciamento completo de atas e acompanhamento de ações
"""
import streamlit as st
from database import DatabaseManager
from utils import formatar_data, confirmar_acao, calcular_duracao_reuniao, status_acao
from datetime import datetime, timedelta
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Atas de Reunião",
    page_icon="📋",
    layout="wide"
)

# Inicializar banco
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# CSS customizado
st.markdown("""
    <style>
    .ata-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2ecc71;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .ata-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transition: all 0.2s;
    }
    .titulo-ata {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .acao-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .participante-badge {
        background-color: #3498db;
        color: white;
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 12px;
        margin-right: 5px;
        display: inline-block;
        margin-bottom: 5px;
    }
    .secao-ata {
        background-color: #ecf0f1;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📋 Gerenciamento de Atas de Reunião")
st.markdown("Documente reuniões e acompanhe ações e decisões")
st.markdown("---")

# Sidebar - Filtros e Ações
with st.sidebar:
    st.header("🎯 Ações")
    
    modo = st.radio(
        "Selecione o modo:",
        ["📋 Listar Atas", "➕ Nova Ata", "✅ Ações Pendentes", "📊 Relatório"],
        index=0
    )
    
    st.markdown("---")
    
    # Estatísticas
    st.subheader("📊 Estatísticas")
    stats = db.obter_estatisticas()
    st.metric("Total de Atas", stats['total_atas'])
    
    acoes_pendentes = db.obter_acoes_pendentes()
    st.metric("Ações Pendentes", len(acoes_pendentes),
             delta="Requer atenção" if len(acoes_pendentes) > 0 else "Tudo OK",
             delta_color="inverse")

# ==================== MODO: NOVA ATA ====================
if modo == "➕ Nova Ata":
    st.subheader("✍️ Criar Nova Ata de Reunião")
    
    with st.form("form_nova_ata", clear_on_submit=True):
        # Informações básicas
        st.markdown("### 📌 Informações Básicas")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            titulo = st.text_input(
                "Título da Reunião *",
                placeholder="Ex: Reunião de Planejamento Semanal",
                help="Título descritivo da reunião"
            )
        
        with col2:
            data_reuniao = st.date_input(
                "Data da Reunião *",
                value=datetime.now()
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            horario_inicio = st.time_input(
                "Horário de Início",
                value=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0).time()
            )
        
        with col2:
            horario_fim = st.time_input(
                "Horário de Término",
                value=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0).time()
            )
        
        # Participantes
        st.markdown("### 👥 Participantes")
        participantes_input = st.text_area(
            "Lista de Participantes (um por linha)",
            placeholder="João Silva\nMaria Santos\nPedro Oliveira",
            height=100,
            help="Digite o nome de cada participante em uma linha separada"
        )
        
        st.markdown("---")
        
        # Pauta
        st.markdown("### 📝 Pauta")
        pauta = st.text_area(
            "Pauta da Reunião",
            placeholder="1. Revisão do status do projeto\n2. Discussão de novos requisitos\n3. Definição de próximos passos",
            height=150
        )
        
        # Discussões
        st.markdown("### 💬 Discussões")
        discussoes = st.text_area(
            "Principais Discussões",
            placeholder="Descreva os principais pontos discutidos durante a reunião...",
            height=200
        )
        
        # Decisões
        st.markdown("### ✅ Decisões Tomadas")
        decisoes = st.text_area(
            "Decisões e Conclusões",
            placeholder="Liste as principais decisões tomadas...",
            height=150
        )
        
        # Ações
        st.markdown("### 🎯 Plano de Ação")
        st.info("💡 Você poderá adicionar ações específicas após criar a ata")
        
        # Próxima reunião
        col1, col2 = st.columns(2)
        
        with col1:
            agendar_proxima = st.checkbox("Agendar próxima reunião?")
        
        with col2:
            proxima_reuniao = None
            if agendar_proxima:
                proxima_reuniao = st.date_input(
                    "Data da Próxima Reunião",
                    value=datetime.now() + timedelta(days=7)
                )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("💾 Salvar Ata", type="primary", use_container_width=True)
        
        if submitted:
            if not titulo:
                st.error("⚠️ O título é obrigatório!")
            else:
                try:
                    # Processar participantes
                    participantes = [p.strip() for p in participantes_input.split('\n') if p.strip()]
                    
                    ata_id = db.criar_ata(
                        titulo=titulo,
                        data_reuniao=data_reuniao.isoformat(),
                        horario_inicio=horario_inicio.strftime("%H:%M:%S"),
                        horario_fim=horario_fim.strftime("%H:%M:%S"),
                        participantes=participantes,
                        pauta=pauta if pauta else None,
                        discussoes=discussoes if discussoes else None,
                        decisoes=decisoes if decisoes else None,
                        proxima_reuniao=proxima_reuniao.isoformat() if proxima_reuniao else None
                    )
                    
                    st.success(f"✅ Ata #{ata_id} criada com sucesso!")
                    st.balloons()
                    
                    # Calcular duração
                    duracao = calcular_duracao_reuniao(
                        horario_inicio.strftime("%H:%M:%S"),
                        horario_fim.strftime("%H:%M:%S")
                    )
                    st.info(f"⏱️ Duração da reunião: {duracao}")
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar ata: {str(e)}")

# ==================== MODO: LISTAR ATAS ====================
elif modo == "📋 Listar Atas":
    st.subheader("📚 Histórico de Atas")
    
    # Filtro de período
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        data_inicio = st.date_input(
            "Data Início",
            value=datetime.now() - timedelta(days=30)
        )
    
    with col2:
        data_fim = st.date_input(
            "Data Fim",
            value=datetime.now()
        )
    
    with col3:
        if st.button("🔍 Filtrar", use_container_width=True):
            st.rerun()
    
    # Buscar atas
    if data_inicio and data_fim:
        atas = db.buscar_atas_por_periodo(data_inicio.isoformat(), data_fim.isoformat())
    else:
        atas = db.listar_atas()
    
    if not atas:
        st.info("📭 Nenhuma ata encontrada no período selecionado.")
        st.markdown("👉 Use o menu lateral para criar sua primeira ata!")
    else:
        st.caption(f"Exibindo {len(atas)} ata(s)")
        
        for ata in atas:
            with st.container():
                # Card da ata
                st.markdown(f"<div class='ata-card'>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(
                        f"<div class='titulo-ata'>📋 Ata #{ata['id']} - {ata['titulo']}</div>",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    data_reuniao_formatada = datetime.fromisoformat(ata['data_reuniao']).strftime("%d/%m/%Y")
                    st.markdown(f"**📅 {data_reuniao_formatada}**")
                
                # Informações da reunião
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if ata['horario_inicio'] and ata['horario_fim']:
                        duracao = calcular_duracao_reuniao(ata['horario_inicio'], ata['horario_fim'])
                        st.caption(f"⏰ {ata['horario_inicio'][:5]} - {ata['horario_fim'][:5]} ({duracao})")
                
                with col2:
                    st.caption(f"👥 {len(ata['participantes'])} participante(s)")
                
                with col3:
                    if ata['acoes']:
                        acoes_pendentes_ata = sum(1 for a in ata['acoes'] if not a.get('concluida', False))
                        st.caption(f"🎯 {acoes_pendentes_ata} ação(ões) pendente(s)")
                
                # Botão para expandir detalhes
                with st.expander("📖 Ver Detalhes Completos"):
                    # Participantes
                    if ata['participantes']:
                        st.markdown("**👥 Participantes:**")
                        participantes_html = "".join([
                            f"<span class='participante-badge'>{p}</span>"
                            for p in ata['participantes']
                        ])
                        st.markdown(participantes_html, unsafe_allow_html=True)
                        st.markdown("")
                    
                    # Pauta
                    if ata['pauta']:
                        st.markdown("**📝 Pauta:**")
                        st.markdown(f"<div class='secao-ata'>{ata['pauta']}</div>", unsafe_allow_html=True)
                    
                    # Discussões
                    if ata['discussoes']:
                        st.markdown("**💬 Discussões:**")
                        st.markdown(f"<div class='secao-ata'>{ata['discussoes']}</div>", unsafe_allow_html=True)
                    
                    # Decisões
                    if ata['decisoes']:
                        st.markdown("**✅ Decisões:**")
                        st.markdown(f"<div class='secao-ata'>{ata['decisoes']}</div>", unsafe_allow_html=True)
                    
                    # Ações
                    if ata['acoes']:
                        st.markdown("**🎯 Plano de Ação:**")
                        for idx, acao in enumerate(ata['acoes']):
                            emoji, status_texto, cor = status_acao(acao.get('prazo', ''))
                            concluida = acao.get('concluida', False)
                            
                            st.markdown(
                                f"""<div class='acao-card' style='opacity: {"0.6" if concluida else "1"};'>
                                <strong>{"✅" if concluida else emoji} {acao.get('descricao', 'Sem descrição')}</strong><br>
                                <small>👤 Responsável: {acao.get('responsavel', 'Não definido')} | 
                                📅 Prazo: {datetime.strptime(acao.get('prazo', ''), '%Y-%m-%d').strftime('%d/%m/%Y') if acao.get('prazo') else 'Não definido'} | 
                                Status: <span style='color: {cor};'>{status_texto if not concluida else 'Concluída'}</span></small>
                                </div>""",
                                unsafe_allow_html=True
                            )
                    
                    # Próxima reunião
                    if ata['proxima_reuniao']:
                        proxima_data = datetime.fromisoformat(ata['proxima_reuniao']).strftime("%d/%m/%Y")
                        st.info(f"📅 Próxima reunião agendada para: **{proxima_data}**")
                
                # Botões de ação
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{ata['id']}", use_container_width=True):
                        st.session_state[f'editando_{ata["id"]}'] = True
                        st.rerun()
                
                with col2:
                    if st.button("🎯 Gerenciar Ações", key=f"acoes_{ata['id']}", use_container_width=True):
                        st.session_state[f'gerenciar_acoes_{ata["id"]}'] = True
                        st.rerun()
                
                with col3:
                    if st.button("📄 Exportar PDF", key=f"export_{ata['id']}", use_container_width=True):
                        st.info("🚧 Funcionalidade em desenvolvimento")
                
                with col4:
                    if st.button("🗑️", key=f"delete_{ata['id']}", help="Deletar"):
                        st.session_state[f'confirmar_delete_{ata["id"]}'] = True
                        st.rerun()
                
                # Confirmação de delete
                if st.session_state.get(f'confirmar_delete_{ata["id"]}', False):
                    if confirmar_acao(
                        f"⚠️ Tem certeza que deseja deletar a ata '{ata['titulo']}'?",
                        f"confirma_{ata['id']}"
                    ):
                        db.deletar_ata(ata['id'])
                        st.success("🗑️ Ata deletada!")
                        del st.session_state[f'confirmar_delete_{ata["id"]}']
                        st.rerun()
                
                # Gerenciar ações
                if st.session_state.get(f'gerenciar_acoes_{ata["id"]}', False):
                    st.markdown("---")
                    st.subheader("🎯 Gerenciar Plano de Ação")
                    
                    # Mostrar ações existentes
                    if ata['acoes']:
                        st.markdown("**Ações Atuais:**")
                        acoes_atualizadas = ata['acoes'].copy()
                        
                        for idx, acao in enumerate(ata['acoes']):
                            col1, col2 = st.columns([4, 1])
                            
                            with col1:
                                concluida = st.checkbox(
                                    f"{acao.get('descricao', '')} - {acao.get('responsavel', '')}",
                                    value=acao.get('concluida', False),
                                    key=f"acao_{ata['id']}_{idx}"
                                )
                                acoes_atualizadas[idx]['concluida'] = concluida
                            
                            with col2:
                                if st.button("🗑️", key=f"del_acao_{ata['id']}_{idx}"):
                                    acoes_atualizadas.pop(idx)
                                    db.atualizar_ata(ata['id'], acoes=acoes_atualizadas)
                                    st.success("Ação removida!")
                                    st.rerun()
                        
                        if st.button("💾 Salvar Status", key=f"save_acoes_{ata['id']}"):
                            db.atualizar_ata(ata['id'], acoes=acoes_atualizadas)
                            st.success("✅ Status das ações atualizado!")
                            st.rerun()
                    
                    st.markdown("---")
                    
                    # Adicionar nova ação
                    with st.form(f"form_nova_acao_{ata['id']}"):
                        st.markdown("**➕ Adicionar Nova Ação:**")
                        
                        nova_descricao = st.text_input("Descrição da Ação")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_responsavel = st.text_input("Responsável")
                        with col2:
                            novo_prazo = st.date_input("Prazo", value=datetime.now() + timedelta(days=7))
                        
                        if st.form_submit_button("➕ Adicionar Ação"):
                            if nova_descricao and novo_responsavel:
                                nova_acao = {
                                    'descricao': nova_descricao,
                                    'responsavel': novo_responsavel,
                                    'prazo': novo_prazo.isoformat(),
                                    'concluida': False
                                }
                                
                                acoes_existentes = ata['acoes'] if ata['acoes'] else []
                                acoes_existentes.append(nova_acao)
                                
                                db.atualizar_ata(ata['id'], acoes=acoes_existentes)
                                st.success("✅ Ação adicionada!")
                                st.rerun()
                            else:
                                st.error("Preencha todos os campos!")
                    
                    if st.button("❌ Fechar Gerenciamento", key=f"close_acoes_{ata['id']}"):
                        del st.session_state[f'gerenciar_acoes_{ata["id"]}']
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")

# ==================== MODO: AÇÕES PENDENTES ====================
elif modo == "✅ Ações Pendentes":
    st.subheader("🎯 Ações Pendentes de Todas as Atas")
    
    acoes = db.obter_acoes_pendentes()
    
    if not acoes:
        st.success("🎉 Parabéns! Não há ações pendentes no momento.")
    else:
        st.warning(f"⚠️ Você tem **{len(acoes)}** ação(ões) pendente(s)")
        
        # Agrupar por status
        atrasadas = []
        hoje = []
        proximas = []
        no_prazo = []
        
        for acao in acoes:
            emoji, status_texto, cor = status_acao(acao['prazo'])
            acao['status_info'] = (emoji, status_texto, cor)
            
            if status_texto == "Atrasada":
                atrasadas.append(acao)
            elif status_texto == "Hoje":
                hoje.append(acao)
            elif status_texto == "Próxima":
                proximas.append(acao)
            else:
                no_prazo.append(acao)
        
        # Exibir por prioridade
        if atrasadas:
            st.markdown("### 🔴 Atrasadas")
            for acao in atrasadas:
                st.error(
                    f"**{acao['acao']}** - {acao['responsavel']} | "
                    f"Prazo: {datetime.strptime(acao['prazo'], '%Y-%m-%d').strftime('%d/%m/%Y')} | "
                    f"Ata: {acao['titulo_ata']}"
                )
        
        if hoje:
            st.markdown("### 🟡 Para Hoje")
            for acao in hoje:
                st.warning(
                    f"**{acao['acao']}** - {acao['responsavel']} | "
                    f"Ata: {acao['titulo_ata']}"
                )
        
        if proximas:
            st.markdown("### 🟠 Próximas (3 dias)")
            for acao in proximas:
                st.info(
                    f"**{acao['acao']}** - {acao['responsavel']} | "
                    f"Prazo: {datetime.strptime(acao['prazo'], '%Y-%m-%d').strftime('%d/%m/%Y')} | "
                    f"Ata: {acao['titulo_ata']}"
                )
        
        if no_prazo:
            with st.expander(f"🟢 No Prazo ({len(no_prazo)})"):
                for acao in no_prazo:
                    st.success(
                        f"**{acao['acao']}** - {acao['responsavel']} | "
                        f"Prazo: {datetime.strptime(acao['prazo'], '%Y-%m-%d').strftime('%d/%m/%Y')} | "
                        f"Ata: {acao['titulo_ata']}"
                    )

# ==================== MODO: RELATÓRIO ====================
elif modo == "📊 Relatório":
    st.subheader("📊 Relatório de Reuniões")
    
    atas = db.listar_atas()
    
    if not atas:
        st.info("Sem dados para gerar relatório")
    else:
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Reuniões", len(atas))
        
        with col2:
            total_participantes = sum(len(ata['participantes']) for ata in atas)
            media_participantes = total_participantes / len(atas) if atas else 0
            st.metric("Média de Participantes", f"{media_participantes:.1f}")
        
        with col3:
            todas_acoes = sum(len(ata['acoes']) for ata in atas)
            st.metric("Total de Ações", todas_acoes)
        
        with col4:
            acoes_pendentes = len(db.obter_acoes_pendentes())
            st.metric("Ações Pendentes", acoes_pendentes)
        
        st.markdown("---")
        
        # Tabela de resumo
        st.subheader("📋 Resumo de Reuniões")
        
        dados_tabela = []
        for ata in atas:
            dados_tabela.append({
                'ID': ata['id'],
                'Título': ata['titulo'],
                'Data': datetime.fromisoformat(ata['data_reuniao']).strftime('%d/%m/%Y'),
                'Participantes': len(ata['participantes']),
                'Ações': len(ata['acoes']) if ata['acoes'] else 0
            })
        
        df = pd.DataFrame(dados_tabela)
        st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("💡 Dica: Mantenha suas atas sempre atualizadas e acompanhe as ações regularmente!")