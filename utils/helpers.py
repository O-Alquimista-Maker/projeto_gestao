"""
Funções auxiliares para o sistema
"""
from datetime import datetime
from typing import Dict, Any
import streamlit as st


def formatar_data(data_str: str, formato: str = "%d/%m/%Y %H:%M") -> str:
    """Formata uma data string para exibição"""
    try:
        data = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
        return data.strftime(formato)
    except:
        return data_str


def cor_prioridade(prioridade: str) -> str:
    """Retorna cor baseada na prioridade"""
    cores = {
        'baixa': '#95a5a6',
        'média': '#3498db',
        'alta': '#e74c3c'
    }
    return cores.get(prioridade.lower(), '#3498db')


def emoji_prioridade(prioridade: str) -> str:
    """Retorna emoji baseado na prioridade"""
    emojis = {
        'baixa': '🟢',
        'média': '🟡',
        'alta': '🔴'
    }
    return emojis.get(prioridade.lower(), '⚪')


def exibir_tag(tag: str, cor: str = "#3498db"):
    """Exibe uma tag estilizada"""
    st.markdown(
        f'<span style="background-color: {cor}; color: white; padding: 3px 10px; '
        f'border-radius: 10px; font-size: 12px; margin-right: 5px;">{tag}</span>',
        unsafe_allow_html=True
    )


def confirmar_acao(mensagem: str, chave: str) -> bool:
    """Exibe um diálogo de confirmação"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.warning(mensagem)
    with col2:
        return st.button("✓ Confirmar", key=chave, type="primary")


def cor_severidade(severidade: str) -> str:
    """Retorna cor baseada na severidade"""
    cores = {
        'baixa': '#2ecc71',
        'média': '#f39c12',
        'alta': '#e74c3c',
        'crítica': '#8e44ad'
    }
    return cores.get(severidade.lower(), '#95a5a6')


def emoji_severidade(severidade: str) -> str:
    """Retorna emoji baseado na severidade"""
    emojis = {
        'baixa': '🟢',
        'média': '🟡',
        'alta': '🔴',
        'crítica': '🟣'
    }
    return emojis.get(severidade.lower(), '⚪')


def cor_status(status: str) -> str:
    """Retorna cor baseada no status"""
    cores = {
        'aberta': '#e74c3c',
        'em análise': '#f39c12',
        'resolvida': '#3498db',
        'fechada': '#2ecc71'
    }
    return cores.get(status.lower(), '#95a5a6')


def emoji_status(status: str) -> str:
    """Retorna emoji baseado no status"""
    emojis = {
        'aberta': '🔴',
        'em análise': '🟡',
        'resolvida': '🔵',
        'fechada': '✅'
    }
    return emojis.get(status.lower(), '⚪')


def emoji_tipo_ocorrencia(tipo: str) -> str:
    """Retorna emoji baseado no tipo de ocorrência"""
    emojis = {
        'Incidente': '⚠️',
        'Problema': '❌',
        'Observação': '👁️',
        'Bug': '🐛',
        'Melhoria': '✨',
        'Outro': '📌'
    }
    return emojis.get(tipo, '📌')
def calcular_duracao_reuniao(inicio: str, fim: str) -> str:
    """Calcula a duração da reunião"""
    try:
        formato = "%H:%M:%S" if len(inicio) > 5 else "%H:%M"
        h_inicio = datetime.strptime(inicio, formato)
        h_fim = datetime.strptime(fim, formato)
        
        duracao = h_fim - h_inicio
        
        horas = duracao.seconds // 3600
        minutos = (duracao.seconds % 3600) // 60
        
        if horas > 0:
            return f"{horas}h {minutos}min"
        else:
            return f"{minutos}min"
    except:
        return "N/A"


def status_acao(prazo: str) -> tuple:
    """Retorna o status de uma ação baseado no prazo"""
    try:
        data_prazo = datetime.strptime(prazo, "%Y-%m-%d").date()
        hoje = datetime.now().date()
        
        if data_prazo < hoje:
            return ("🔴", "Atrasada", "#e74c3c")
        elif data_prazo == hoje:
            return ("🟡", "Hoje", "#f39c12")
        elif (data_prazo - hoje).days <= 3:
            return ("🟠", "Próxima", "#e67e22")
        else:
            return ("🟢", "No prazo", "#2ecc71")
    except:
        return ("⚪", "Sem prazo", "#95a5a6")