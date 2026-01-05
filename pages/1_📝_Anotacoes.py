"""
Módulo de Anotações
Gerenciamento completo de anotações com tags, categorias e busca
"""
import streamlit as st
from database import DatabaseManager
from utils import formatar_data, emoji_prioridade, confirmar_acao
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Anotações",
    page_icon="📝",
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
    .anotacao-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .anotacao-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .tag-badge {
        background-color: #3498db;
        color: white;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 5px;
        display: inline-block;
    }
    .prioridade-badge {
        padding: 5px 12px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: bold;
    }
    .titulo-anotacao {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📝 Gerenciamento de Anotações")
st.markdown("Crie, edite e organize suas anotações com tags e categorias")
st.markdown("---")

# Sidebar - Filtros e Ações
with st.sidebar:
    st.header("🎯 Ações")
    
    modo = st.radio(
        "Selecione o modo:",
        ["📋 Listar Anotações", "➕ Nova Anotação", "🔍 Buscar"],
        index=0
    )
    
    st.markdown("---")
    
    if modo == "📋 Listar Anotações":
        st.subheader("🔧 Filtros")
        
        # Filtro de categoria
        categorias = ["Todas"] + db.obter_categorias()
        if not categorias or len(categorias) == 1:
            categorias = ["Todas", "Geral", "Trabalho", "Pessoal", "Estudo"]
        
        filtro_categoria = st.selectbox("Categoria:", categorias)
        
        # Filtro de prioridade
        filtro_prioridade = st.selectbox(
            "Prioridade:",
            ["Todas", "Baixa", "Média", "Alta"]
        )
        
        # Mostrar arquivadas
        mostrar_arquivadas = st.checkbox("Mostrar arquivadas")
        
        st.markdown("---")
        
        # Estatísticas
        st.subheader("📊 Estatísticas")
        stats = db.obter_estatisticas()
        st.metric("Total de Anotações", stats['total_anotacoes'])
        st.metric("Arquivadas", stats['anotacoes_arquivadas'])

# ==================== MODO: NOVA ANOTAÇÃO ====================
if modo == "➕ Nova Anotação":
    st.subheader("✍️ Criar Nova Anotação")
    
    with st.form("form_nova_anotacao", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            titulo = st.text_input(
                "Título *",
                placeholder="Digite o título da anotação...",
                help="Título obrigatório"
            )
        
        with col2:
            categoria = st.selectbox(
                "Categoria",
                ["Geral", "Trabalho", "Pessoal", "Estudo", "Ideias", "Projetos", "Outros"]
            )
        
        conteudo = st.text_area(
            "Conteúdo",
            placeholder="Digite o conteúdo da anotação...\n\nVocê pode usar markdown para formatar!",
            height=300,
            help="Suporta formatação Markdown"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            prioridade = st.select_slider(
                "Prioridade",
                options=["Baixa", "Média", "Alta"],
                value="Média"
            )
        
        with col2:
            tags_input = st.text_input(
                "Tags (separadas por vírgula)",
                placeholder="python, projeto, urgente"
            )
        
        submitted = st.form_submit_button("💾 Salvar Anotação", type="primary", use_container_width=True)
        
        if submitted:
            if not titulo:
                st.error("⚠️ O título é obrigatório!")
            else:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                
                try:
                    anotacao_id = db.criar_anotacao(
                        titulo=titulo,
                        conteudo=conteudo,
                        categoria=categoria,
                        tags=tags,
                        prioridade=prioridade.lower()
                    )
                    st.success(f"✅ Anotação #{anotacao_id} criada com sucesso!")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao criar anotação: {str(e)}")

# ==================== MODO: LISTAR ANOTAÇÕES ====================
elif modo == "📋 Listar Anotações":
    st.subheader("📚 Suas Anotações")
    
    # Buscar anotações
    categoria_filtro = None if filtro_categoria == "Todas" else filtro_categoria
    anotacoes = db.listar_anotacoes(
        arquivada=mostrar_arquivadas,
        categoria=categoria_filtro
    )
    
    # Filtrar por prioridade
    if filtro_prioridade != "Todas":
        anotacoes = [a for a in anotacoes if a['prioridade'].lower() == filtro_prioridade.lower()]
    
    if not anotacoes:
        st.info("📭 Nenhuma anotação encontrada com os filtros selecionados.")
        st.markdown("👉 Use o menu lateral para criar sua primeira anotação!")
    else:
        st.caption(f"Exibindo {len(anotacoes)} anotação(ões)")
        
        for anotacao in anotacoes:
            with st.container():
                # Card da anotação
                col1, col2 = st.columns([5, 1])
                
                with col1:
                    # Título com emoji de prioridade
                    st.markdown(
                        f"<div class='titulo-anotacao'>"
                        f"{emoji_prioridade(anotacao['prioridade'])} {anotacao['titulo']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    # Badge de categoria
                    st.markdown(
                        f"<span class='tag-badge'>{anotacao['categoria']}</span>",
                        unsafe_allow_html=True
                    )
                
                # Conteúdo (preview)
                if anotacao['conteudo']:
                    preview = anotacao['conteudo'][:200]
                    if len(anotacao['conteudo']) > 200:
                        preview += "..."
                    st.markdown(preview)
                
                # Tags
                if anotacao['tags']:
                    st.markdown("**Tags:** " + " ".join([
                        f"<span class='tag-badge'>{tag}</span>" 
                        for tag in anotacao['tags']
                    ]), unsafe_allow_html=True)
                
                # Informações adicionais
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                
                with col1:
                    st.caption(f"📅 Criado: {anotacao['data_criacao'][:16].replace('T', ' ')}")
                
                with col2:
                    st.caption(f"✏️ Modificado: {anotacao['data_modificacao'][:16].replace('T', ' ')}")
                
                # Botões de ação
                with col3:
                    if st.button("✏️", key=f"edit_{anotacao['id']}", help="Editar"):
                        st.session_state[f'editando_{anotacao["id"]}'] = True
                        st.rerun()
                
                with col4:
                    icone_arquivo = "📂" if anotacao['arquivada'] else "📦"
                    tooltip = "Desarquivar" if anotacao['arquivada'] else "Arquivar"
                    if st.button(icone_arquivo, key=f"archive_{anotacao['id']}", help=tooltip):
                        db.arquivar_anotacao(anotacao['id'], not anotacao['arquivada'])
                        st.success("✅ Anotação atualizada!")
                        st.rerun()
                
                with col5:
                    if st.button("🗑️", key=f"delete_{anotacao['id']}", help="Deletar"):
                        st.session_state[f'confirmar_delete_{anotacao["id"]}'] = True
                        st.rerun()
                
                # Confirmação de delete
                if st.session_state.get(f'confirmar_delete_{anotacao["id"]}', False):
                    if confirmar_acao(
                        f"⚠️ Tem certeza que deseja deletar a anotação '{anotacao['titulo']}'?",
                        f"confirma_{anotacao['id']}"
                    ):
                        db.deletar_anotacao(anotacao['id'])
                        st.success("🗑️ Anotação deletada!")
                        del st.session_state[f'confirmar_delete_{anotacao["id"]}']
                        st.rerun()
                
                # Modo edição
                if st.session_state.get(f'editando_{anotacao["id"]}', False):
                    st.markdown("---")
                    with st.form(f"form_edit_{anotacao['id']}"):
                        st.subheader("✏️ Editando Anotação")
                        
                        novo_titulo = st.text_input("Título", value=anotacao['titulo'])
                        novo_conteudo = st.text_area("Conteúdo", value=anotacao['conteudo'], height=200)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            nova_categoria = st.selectbox(
                                "Categoria",
                                ["Geral", "Trabalho", "Pessoal", "Estudo", "Ideias", "Projetos", "Outros"],
                                index=["Geral", "Trabalho", "Pessoal", "Estudo", "Ideias", "Projetos", "Outros"].index(anotacao['categoria']) if anotacao['categoria'] in ["Geral", "Trabalho", "Pessoal", "Estudo", "Ideias", "Projetos", "Outros"] else 0
                            )
                        
                        with col2:
                            nova_prioridade = st.select_slider(
                                "Prioridade",
                                options=["Baixa", "Média", "Alta"],
                                value=anotacao['prioridade'].capitalize()
                            )
                        
                        novas_tags = st.text_input(
                            "Tags (separadas por vírgula)",
                            value=", ".join(anotacao['tags']) if anotacao['tags'] else ""
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True):
                                tags_list = [tag.strip() for tag in novas_tags.split(",") if tag.strip()]
                                db.atualizar_anotacao(
                                    anotacao['id'],
                                    titulo=novo_titulo,
                                    conteudo=novo_conteudo,
                                    categoria=nova_categoria,
                                    tags=tags_list,
                                    prioridade=nova_prioridade.lower()
                                )
                                st.success("✅ Anotação atualizada!")
                                del st.session_state[f'editando_{anotacao["id"]}']
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("❌ Cancelar", use_container_width=True):
                                del st.session_state[f'editando_{anotacao["id"]}']
                                st.rerun()
                
                st.markdown("---")

# ==================== MODO: BUSCAR ====================
elif modo == "🔍 Buscar":
    st.subheader("🔎 Busca Avançada")
    
    termo_busca = st.text_input(
        "Digite o termo de busca:",
        placeholder="Busque por título ou conteúdo...",
        help="A busca é feita no título e no conteúdo das anotações"
    )
    
    if termo_busca:
        resultados = db.buscar_anotacoes(termo_busca)
        
        if resultados:
            st.success(f"✅ Encontradas {len(resultados)} anotação(ões)")
            
            for anotacao in resultados:
                with st.expander(f"{emoji_prioridade(anotacao['prioridade'])} {anotacao['titulo']}"):
                    st.markdown(f"**Categoria:** {anotacao['categoria']}")
                    st.markdown(f"**Prioridade:** {anotacao['prioridade'].capitalize()}")
                    
                    if anotacao['tags']:
                        st.markdown("**Tags:** " + ", ".join(anotacao['tags']))
                    
                    st.markdown("---")
                    st.markdown(anotacao['conteudo'])
                    
                    st.caption(f"📅 Criado em: {anotacao['data_criacao'][:16].replace('T', ' ')}")
        else:
            st.warning("⚠️ Nenhuma anotação encontrada com esse termo.")
    else:
        st.info("👆 Digite algo no campo acima para buscar")

# Footer
st.markdown("---")
st.caption("💡 Dica: Use Markdown para formatar suas anotações! **Negrito**, *Itálico*, `código`, etc.")