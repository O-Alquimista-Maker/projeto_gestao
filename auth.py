"""
Sistema de autenticação
"""
import streamlit as st
import hashlib
from datetime import datetime

SENHA_MASTER_HASH = "7ed50aae9f147f4ce1d6f04ed03536ada13b705bc3ce6653ebb75df8e45747c4"

def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha: str) -> bool:
    return gerar_hash_senha(senha) == SENHA_MASTER_HASH

def login_simples():
    if st.session_state.get('autenticado', False):
        return True
    
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        .login-title {
            color: white;
            text-align: center;
            font-size: 2rem;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div class='login-container'>
                <div class='login-title'>
                    🔐 Sistema de Gestão
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔒 Acesso Restrito")
        st.markdown("Digite a senha master para acessar o sistema")
        
        senha = st.text_input(
            "Senha:",
            type="password",
            placeholder="Digite a senha master",
            key="senha_input"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔓 Entrar", use_container_width=True, type="primary"):
                if senha:
                    if verificar_senha(senha):
                        st.session_state['autenticado'] = True
                        st.session_state['login_time'] = datetime.now()
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Senha incorreta!")
                else:
                    st.warning("⚠️ Digite a senha!")
        
        with col_btn2:
            if st.button("ℹ️ Ajuda", use_container_width=True):
                st.info("Entre em contato com o administrador do sistema para obter a senha de acesso.")
        
        st.markdown("---")
        st.caption("🔒 Sistema protegido por autenticação")
    
    return False

def logout():
    st.session_state['autenticado'] = False
    if 'login_time' in st.session_state:
        del st.session_state['login_time']
    st.rerun()

def exibir_info_usuario():
    if st.session_state.get('autenticado', False):
        with st.sidebar:
            st.markdown("---")
            st.success("✅ Sessão ativa")
            
            if 'login_time' in st.session_state:
                tempo_login = datetime.now() - st.session_state['login_time']
                horas = tempo_login.seconds // 3600
                minutos = (tempo_login.seconds % 3600) // 60
                st.caption(f"⏱️ Logado há: {horas}h {minutos}min")
            
            if st.button("🚪 Sair", use_container_width=True):
                logout()