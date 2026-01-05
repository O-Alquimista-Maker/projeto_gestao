"""
Sistema de Gestão - Anotações, Ocorrências e Atas de Reunião
Aplicação principal com dashboard
"""
import streamlit as st
from database import DatabaseManager
from datetime import datetime
import plotly.graph_objects as go
from utils.components import exibir_logo_sidebar, exibir_assinatura_footer
from auth import login_simples, exibir_info_usuario
from config import EMPRESA

# Configuração da página
st.set_page_config(
    page_title=f"Sistema de Gestão - {EMPRESA['nome']}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== AUTENTICAÇÃO ====================
if not login_simples():
    st.stop()

# Inicializar o banco de dados
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# ==================== SIDEBAR COM LOGO ====================
exibir_logo_sidebar()
exibir_info_usuario()

with st.sidebar:
    st.title("🎯 Menu Principal")
    st.markdown("---")
    st.info("**Bem-vindo ao Sistema de Gestão!**")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    st.caption(f"🕐 {datetime.now().strftime('%H:%M')}")

# Header
st.title("📊 Sistema de Gestão Integrado")
st.markdown("Dashboard de Controle e Monitoramento")
st.markdown("---")

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

# Gráfico
st.subheader("📊 Distribuição de Registros")

labels = ['Anotações', 'Ocorrências', 'Atas']
values = [stats['total_anotacoes'], stats['total_ocorrencias'], stats['total_atas']]
colors = ['#3498db', '#e74c3c', '#2ecc71']

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.4,
    marker=dict(colors=colors),
    textinfo='label+percent'
)])

fig.update_layout(title_text="Visão Geral do Sistema", height=400)
st.plotly_chart(fig, use_container_width=True)

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

# Footer com assinatura
exibir_assinatura_footer(pagina="Dashboard")