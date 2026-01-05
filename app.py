"""
Sistema de Gestão - Anotações, Ocorrências e Atas de Reunião
Aplicação principal com dashboard
"""
import streamlit as st
from database import DatabaseManager
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar o banco de dados
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">📊 Sistema de Gestão Integrado</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/management.png", width=100)
    st.title("🎯 Menu Principal")
    st.markdown("---")
    
    st.info("""
    **Bem-vindo ao Sistema de Gestão!**
    
    Gerencie suas anotações, ocorrências e atas de reunião de forma integrada.
    """)
    
    st.markdown("---")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    st.caption(f"🕐 {datetime.now().strftime('%H:%M')}")

# Dashboard Principal
st.header("📈 Dashboard Geral")

# Obter estatísticas
stats = db.obter_estatisticas()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📝 Anotações Ativas",
        value=stats['total_anotacoes'],
        delta=f"{stats['anotacoes_arquivadas']} arquivadas"
    )

with col2:
    st.metric(
        label="🚨 Ocorrências Abertas",
        value=stats['ocorrencias_abertas'],
        delta=f"{stats['total_ocorrencias']} total",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="📋 Atas Registradas",
        value=stats['total_atas'],
        delta="Reuniões documentadas"
    )

with col4:
    total_itens = stats['total_anotacoes'] + stats['total_ocorrencias'] + stats['total_atas']
    st.metric(
        label="📊 Total de Registros",
        value=total_itens,
        delta="Todos os módulos"
    )

st.markdown("---")

# Seção de gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribuição de Registros")
    
    # Gráfico de pizza
    labels = ['Anotações', 'Ocorrências', 'Atas']
    values = [stats['total_anotacoes'], stats['total_ocorrencias'], stats['total_atas']]
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig.update_layout(
        title_text="Visão Geral do Sistema",
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Status das Ocorrências")
    
    # Simular dados de ocorrências por status (você pode buscar do banco depois)
    status_labels = ['Abertas', 'Em Análise', 'Resolvidas', 'Fechadas']
    status_values = [
        stats['ocorrencias_abertas'],
        max(0, stats['total_ocorrencias'] - stats['ocorrencias_abertas'] - 2),
        1,
        1
    ]
    
    fig2 = go.Figure(data=[go.Bar(
        x=status_labels,
        y=status_values,
        marker=dict(
            color=['#e74c3c', '#f39c12', '#3498db', '#2ecc71'],
            line=dict(color='rgb(8,48,107)', width=1.5)
        ),
        text=status_values,
        textposition='auto',
    )])
    
    fig2.update_layout(
        title_text="Ocorrências por Status",
        height=400,
        yaxis_title="Quantidade",
        xaxis_title="Status"
    )
    
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Atividades recentes
st.subheader("🕐 Atividades Recentes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📝 Últimas Anotações")
    anotacoes_recentes = db.listar_anotacoes()[:5]
    
    if anotacoes_recentes:
        for anotacao in anotacoes_recentes:
            with st.container():
                st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <strong>{anotacao['titulo']}</strong><br>
                    <small>📅 {anotacao['data_criacao'][:16].replace('T', ' às ')}</small><br>
                    <span style='background-color: #3498db; color: white; padding: 2px 8px; border-radius: 5px; font-size: 11px;'>
                        {anotacao['categoria']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma anotação cadastrada ainda.")

with col2:
    st.markdown("### 📋 Últimas Atas")
    st.info("Em breve: lista de atas recentes")

st.markdown("---")

# Ações rápidas
st.subheader("⚡ Ações Rápidas")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Nova Anotação", use_container_width=True, type="primary"):
        st.switch_page("pages/1_📝_Anotacoes.py")

with col2:
    if st.button("🚨 Registrar Ocorrência", use_container_width=True):
        st.switch_page("pages/2_🚨_Ocorrencias.py")

with col3:
    if st.button("📋 Nova Ata", use_container_width=True):
        st.switch_page("pages/3_📋_Atas_Reuniao.py")

st.markdown("---")

# Informações do sistema
with st.expander("ℹ️ Informações do Sistema"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📌 Módulos Disponíveis:**
        - ✅ Anotações
        - ✅ Ocorrências
        - ✅ Atas de Reunião
        
        **🔧 Recursos:**
        - Sistema de tags
        - Busca avançada
        - Filtros inteligentes
        - Exportação de dados
        """)
    
    with col2:
        st.markdown("""
        **💾 Banco de Dados:**
        - SQLite Local
        - Backup automático
        - Zero configuração
        
        **🎨 Interface:**
        - Design responsivo
        - Gráficos interativos
        - Navegação intuitiva
        """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #7f8c8d;'>Sistema de Gestão Integrado v1.0 | "
    "Desenvolvido com Streamlit 🚀</p>",
    unsafe_allow_html=True
)