"""
Módulo de Ocorrências
Gerenciamento completo de ocorrências e incidentes
"""
import streamlit as st
from utils.components import exibir_logo_sidebar, exibir_assinatura_footer
from auth import login_simples, exibir_info_usuario
from database import DatabaseManager
from utils import (formatar_data, emoji_severidade, cor_severidade, 
                   emoji_status, cor_status, emoji_tipo_ocorrencia, confirmar_acao)
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Ocorrências",
    page_icon="🚨",
    layout="wide"
)

if not login_simples():
    st.stop()

# Inicializar banco
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# CSS customizado
st.markdown("""
    <style>
    .ocorrencia-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .ocorrencia-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .status-badge {
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        display: inline-block;
    }
    .severidade-badge {
        padding: 5px 15px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
        color: white;
        display: inline-block;
        margin-left: 10px;
    }
    .titulo-ocorrencia {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .alerta-critico {
        background-color: #ffe6e6;
        border-left: 5px solid #e74c3c;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🚨 Gerenciamento de Ocorrências")
st.markdown("Registre e acompanhe incidentes, problemas e observações")
exibir_logo_sidebar()
exibir_info_usuario()

st.markdown("---")

# Verificar ocorrências críticas abertas
ocorrencias_criticas = db.obter_ocorrencias_criticas_abertas()
if ocorrencias_criticas:
    st.markdown(
        f"""<div class='alerta-critico'>
        <strong>⚠️ ATENÇÃO: {len(ocorrencias_criticas)} ocorrência(s) crítica(s) em aberto!</strong><br>
        Por favor, revise e tome as ações necessárias.
        </div>""",
        unsafe_allow_html=True
    )

# Sidebar - Filtros e Ações
with st.sidebar:
    st.header("🎯 Ações")
    
    modo = st.radio(
        "Selecione o modo:",
        ["📋 Listar Ocorrências", "➕ Nova Ocorrência", "📊 Dashboard"],
        index=0
    )
    
    st.markdown("---")
    
    if modo == "📋 Listar Ocorrências":
        st.subheader("🔧 Filtros")
        
        # Filtros
        filtro_status = st.selectbox(
            "Status:",
            ["Todos", "Aberta", "Em Análise", "Resolvida", "Fechada"]
        )
        
        filtro_severidade = st.selectbox(
            "Severidade:",
            ["Todas", "Baixa", "Média", "Alta", "Crítica"]
        )
        
        filtro_tipo = st.selectbox(
            "Tipo:",
            ["Todos", "Incidente", "Problema", "Observação", "Bug", "Melhoria", "Outro"]
        )
        
        st.markdown("---")
    
    # Estatísticas
    st.subheader("📊 Estatísticas")
    stats = db.obter_estatisticas()
    st.metric("Total de Ocorrências", stats['total_ocorrencias'])
    st.metric("Abertas", stats['ocorrencias_abertas'], 
             delta="Requer atenção" if stats['ocorrencias_abertas'] > 0 else "Tudo OK",
             delta_color="inverse")

# ==================== MODO: NOVA OCORRÊNCIA ====================
if modo == "➕ Nova Ocorrência":
    st.subheader("📝 Registrar Nova Ocorrência")
    
    with st.form("form_nova_ocorrencia", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            tipo = st.selectbox(
                "Tipo de Ocorrência *",
                ["Incidente", "Problema", "Observação", "Bug", "Melhoria", "Outro"],
                help="Selecione o tipo da ocorrência"
            )
        
        with col2:
            severidade = st.select_slider(
                "Severidade *",
                options=["Baixa", "Média", "Alta", "Crítica"],
                value="Média"
            )
        
        descricao = st.text_area(
            "Descrição da Ocorrência *",
            placeholder="Descreva detalhadamente o que aconteceu...",
            height=200,
            help="Quanto mais detalhes, melhor para análise"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            data_ocorrencia = st.date_input(
                "Data da Ocorrência",
                value=datetime.now(),
                help="Quando o problema ocorreu"
            )
        
        with col2:
            hora_ocorrencia = st.time_input(
                "Hora da Ocorrência",
                value=datetime.now().time()
            )
        
        responsavel = st.text_input(
            "Responsável (opcional)",
            placeholder="Nome do responsável pela resolução"
        )
        
        solucao = st.text_area(
            "Solução Proposta (opcional)",
            placeholder="Descreva a solução ou ações tomadas...",
            height=150
        )
        
        submitted = st.form_submit_button("💾 Registrar Ocorrência", type="primary", use_container_width=True)
        
        if submitted:
            if not descricao:
                st.error("⚠️ A descrição é obrigatória!")
            else:
                try:
                    # Combinar data e hora
                    data_hora = datetime.combine(data_ocorrencia, hora_ocorrencia)
                    
                    ocorrencia_id = db.criar_ocorrencia(
                        tipo=tipo,
                        descricao=descricao,
                        severidade=severidade.lower(),
                        data_ocorrencia=data_hora.isoformat(),
                        responsavel=responsavel if responsavel else None,
                        solucao=solucao if solucao else None
                    )
                    
                    st.success(f"✅ Ocorrência #{ocorrencia_id} registrada com sucesso!")
                    
                    if severidade == "Crítica":
                        st.warning("⚠️ Ocorrência CRÍTICA registrada! Requer atenção imediata.")
                    
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao registrar ocorrência: {str(e)}")

# ==================== MODO: LISTAR OCORRÊNCIAS ====================
elif modo == "📋 Listar Ocorrências":
    st.subheader("📚 Registro de Ocorrências")
    
    # Buscar ocorrências com filtros
    status_filtro = None if filtro_status == "Todos" else filtro_status
    severidade_filtro = None if filtro_severidade == "Todas" else filtro_severidade
    tipo_filtro = None if filtro_tipo == "Todos" else filtro_tipo
    
    ocorrencias = db.listar_ocorrencias(
        status=status_filtro,
        severidade=severidade_filtro,
        tipo=tipo_filtro
    )
    
    if not ocorrencias:
        st.info("📭 Nenhuma ocorrência encontrada com os filtros selecionados.")
        st.markdown("👉 Use o menu lateral para registrar uma nova ocorrência!")
    else:
        st.caption(f"Exibindo {len(ocorrencias)} ocorrência(s)")
        
        for ocorrencia in ocorrencias:
            with st.container():
                # Borda colorida baseada na severidade
                border_color = cor_severidade(ocorrencia['severidade'])
                
                st.markdown(f"""
                    <div style='border-left: 5px solid {border_color}; padding-left: 15px;'>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([4, 2])
                
                with col1:
                    # Título com emoji
                    st.markdown(
                        f"<div class='titulo-ocorrencia'>"
                        f"{emoji_tipo_ocorrencia(ocorrencia['tipo'])} "
                        f"Ocorrência #{ocorrencia['id']} - {ocorrencia['tipo']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    # Badges de status e severidade
                    st.markdown(
                        f"<span class='status-badge' style='background-color: {cor_status(ocorrencia['status'])};'>"
                        f"{emoji_status(ocorrencia['status'])} {ocorrencia['status'].upper()}"
                        f"</span>"
                        f"<span class='severidade-badge' style='background-color: {cor_severidade(ocorrencia['severidade'])};'>"
                        f"{emoji_severidade(ocorrencia['severidade'])} {ocorrencia['severidade'].upper()}"
                        f"</span>",
                        unsafe_allow_html=True
                    )
                
                # Descrição
                st.markdown(f"**Descrição:** {ocorrencia['descricao']}")
                
                # Solução (se houver)
                if ocorrencia['solucao']:
                    with st.expander("💡 Ver Solução"):
                        st.markdown(ocorrencia['solucao'])
                
                # Informações adicionais
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    data_ocorr = ocorrencia['data_ocorrencia'][:16].replace('T', ' às ')
                    st.caption(f"📅 Ocorreu em: {data_ocorr}")
                
                with col2:
                    data_reg = ocorrencia['data_registro'][:16].replace('T', ' às ')
                    st.caption(f"📝 Registrado em: {data_reg}")
                
                with col3:
                    if ocorrencia['responsavel']:
                        st.caption(f"👤 Responsável: {ocorrencia['responsavel']}")
                
                # Botões de ação
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                
                with col1:
                    if st.button("✏️ Editar", key=f"edit_{ocorrencia['id']}", use_container_width=True):
                        st.session_state[f'editando_{ocorrencia["id"]}'] = True
                        st.rerun()
                
                with col2:
                    novo_status = st.selectbox(
                        "Status",
                        ["Aberta", "Em Análise", "Resolvida", "Fechada"],
                        index=["aberta", "em análise", "resolvida", "fechada"].index(ocorrencia['status']),
                        key=f"status_{ocorrencia['id']}"
                    )
                    if novo_status.lower() != ocorrencia['status']:
                        if st.button("💾", key=f"save_status_{ocorrencia['id']}", help="Salvar status"):
                            db.atualizar_ocorrencia(ocorrencia['id'], status=novo_status.lower())
                            st.success("✅ Status atualizado!")
                            st.rerun()
                
                with col3:
                    if ocorrencia['status'] != 'fechada':
                        if st.button("✅ Fechar", key=f"close_{ocorrencia['id']}", use_container_width=True):
                            db.atualizar_ocorrencia(ocorrencia['id'], status='fechada')
                            st.success("✅ Ocorrência fechada!")
                            st.rerun()
                
                with col4:
                    pass  # Espaço reservado
                
                with col5:
                    if st.button("🗑️", key=f"delete_{ocorrencia['id']}", help="Deletar"):
                        st.session_state[f'confirmar_delete_{ocorrencia["id"]}'] = True
                        st.rerun()
                
                # Confirmação de delete
                if st.session_state.get(f'confirmar_delete_{ocorrencia["id"]}', False):
                    if confirmar_acao(
                        f"⚠️ Tem certeza que deseja deletar a ocorrência #{ocorrencia['id']}?",
                        f"confirma_{ocorrencia['id']}"
                    ):
                        db.deletar_ocorrencia(ocorrencia['id'])
                        st.success("🗑️ Ocorrência deletada!")
                        del st.session_state[f'confirmar_delete_{ocorrencia["id"]}']
                        st.rerun()
                
                # Modo edição
                if st.session_state.get(f'editando_{ocorrencia["id"]}', False):
                    st.markdown("---")
                    with st.form(f"form_edit_{ocorrencia['id']}"):
                        st.subheader("✏️ Editando Ocorrência")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            novo_tipo = st.selectbox(
                                "Tipo",
                                ["Incidente", "Problema", "Observação", "Bug", "Melhoria", "Outro"],
                                index=["Incidente", "Problema", "Observação", "Bug", "Melhoria", "Outro"].index(ocorrencia['tipo']) if ocorrencia['tipo'] in ["Incidente", "Problema", "Observação", "Bug", "Melhoria", "Outro"] else 0
                            )
                        
                        with col2:
                            nova_severidade = st.select_slider(
                                "Severidade",
                                options=["Baixa", "Média", "Alta", "Crítica"],
                                value=ocorrencia['severidade'].capitalize()
                            )
                        
                        nova_descricao = st.text_area(
                            "Descrição",
                            value=ocorrencia['descricao'],
                            height=150
                        )
                        
                        novo_responsavel = st.text_input(
                            "Responsável",
                            value=ocorrencia['responsavel'] if ocorrencia['responsavel'] else ""
                        )
                        
                        nova_solucao = st.text_area(
                            "Solução",
                            value=ocorrencia['solucao'] if ocorrencia['solucao'] else "",
                            height=150
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True):
                                db.atualizar_ocorrencia(
                                    ocorrencia['id'],
                                    tipo=novo_tipo,
                                    descricao=nova_descricao,
                                    severidade=nova_severidade.lower(),
                                    responsavel=novo_responsavel if novo_responsavel else None,
                                    solucao=nova_solucao if nova_solucao else None
                                )
                                st.success("✅ Ocorrência atualizada!")
                                del st.session_state[f'editando_{ocorrencia["id"]}']
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                del st.session_state[f'editando_{ocorrencia["id"]}']
                                st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("---")

# ==================== MODO: DASHBOARD ====================
elif modo == "📊 Dashboard":
    st.subheader("📊 Dashboard de Ocorrências")
    
    # Obter dados
    todas_ocorrencias = db.listar_ocorrencias()
    stats_status = db.obter_ocorrencias_por_status()
    stats_severidade = db.obter_ocorrencias_por_severidade()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(todas_ocorrencias)
        st.metric("Total de Ocorrências", total)
    
    with col2:
        abertas = stats_status.get('aberta', 0)
        st.metric("Abertas", abertas, delta="Atenção" if abertas > 0 else "OK", delta_color="inverse")
    
    with col3:
        em_analise = stats_status.get('em análise', 0)
        st.metric("Em Análise", em_analise)
    
    with col4:
        fechadas = stats_status.get('fechada', 0)
        st.metric("Fechadas", fechadas, delta="Resolvidas", delta_color="normal")
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Ocorrências por Status")
        
        if stats_status:
            labels = list(stats_status.keys())
            values = list(stats_status.values())
            colors = [cor_status(s) for s in labels]
            
            fig = go.Figure(data=[go.Pie(
                labels=[l.capitalize() for l in labels],
                values=values,
                hole=0.4,
                marker=dict(colors=colors),
                textinfo='label+value+percent'
            )])
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    with col2:
        st.subheader("⚠️ Ocorrências por Severidade")
        
        if stats_severidade:
            labels = list(stats_severidade.keys())
            values = list(stats_severidade.values())
            colors = [cor_severidade(s) for s in labels]
            
            fig = go.Figure(data=[go.Bar(
                x=[l.capitalize() for l in labels],
                y=values,
                marker=dict(color=colors),
                text=values,
                textposition='auto'
            )])
            
            fig.update_layout(
                height=400,
                yaxis_title="Quantidade",
                xaxis_title="Severidade"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados para exibir")
    
    st.markdown("---")
    
    # Timeline
    if todas_ocorrencias:
        st.subheader("📅 Timeline de Ocorrências")
        
        df = pd.DataFrame(todas_ocorrencias)
        df['data_ocorrencia'] = pd.to_datetime(df['data_ocorrencia'])
        df['data'] = df['data_ocorrencia'].dt.date
        
        timeline = df.groupby('data').size().reset_index(name='quantidade')
        
        fig = px.line(
            timeline,
            x='data',
            y='quantidade',
            title='Ocorrências ao Longo do Tempo',
            markers=True
        )
        
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Número de Ocorrências",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("💡 Dica: Mantenha suas ocorrências sempre atualizadas para melhor rastreabilidade!")