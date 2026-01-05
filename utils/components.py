"""
Componentes visuais reutilizáveis
"""
import streamlit as st
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from config import EMPRESA, DESENVOLVEDOR, VERSAO, DATA_VERSAO
except:
    EMPRESA = {
        'nome': 'Sua Empresa',
        'logo_url': 'https://via.placeholder.com/150x150.png?text=LOGO',
        'site': 'www.suaempresa.com.br'
    }
    DESENVOLVEDOR = {
        'nome': 'Seu Nome',
        'cargo': 'Desenvolvedor Python',
        'email': 'seuemail@exemplo.com'
    }
    VERSAO = '1.0.0'
    DATA_VERSAO = '06/01/2026'


def exibir_logo_sidebar():
    with st.sidebar:
        try:
            if os.path.exists(EMPRESA.get('logo_local', '')):
                st.image(EMPRESA['logo_local'], width=180)
            else:
                st.image(EMPRESA['logo_url'], width=180)
        except:
            st.image(EMPRESA['logo_url'], width=180)
        
        st.markdown(f"""
            <div style='text-align: center; margin-top: -10px;'>
                <h3 style='color: #1f77b4; margin: 0;'>{EMPRESA['nome']}</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")


def exibir_info_empresa_sidebar():
    with st.sidebar:
        st.markdown("---")
        
        with st.expander("ℹ️ Informações da Empresa"):
            st.markdown(f"""
            **{EMPRESA['nome']}**
            
            🌐 Site: [{EMPRESA.get('site', 'N/A')}](https://{EMPRESA.get('site', '#')})
            
            📧 Email: {EMPRESA.get('email', 'N/A')}
            
            📊 Sistema de Gestão v{VERSAO}
            """)


def exibir_assinatura_footer(pagina: str = ""):
    st.markdown("---")
    
    st.markdown("""
        <style>
        .footer-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .footer-title {
            color: white;
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
        }
        .footer-info {
            color: white;
            font-size: 0.9rem;
            text-align: center;
            line-height: 1.8;
        }
        .footer-links {
            text-align: center;
            margin-top: 15px;
        }
        .footer-link {
            color: white;
            text-decoration: none;
            margin: 0 10px;
            padding: 5px 15px;
            background-color: rgba(255,255,255,0.2);
            border-radius: 15px;
            transition: all 0.3s;
            display: inline-block;
            font-size: 0.85rem;
        }
        .footer-link:hover {
            background-color: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        .footer-copyright {
            text-align: center;
            color: rgba(255,255,255,0.8);
            font-size: 0.75rem;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }
        </style>
    """, unsafe_allow_html=True)
    
    links = []
    
    if DESENVOLVEDOR.get('email'):
        links.append(f'<a href="mailto:{DESENVOLVEDOR["email"]}" class="footer-link" target="_blank">📧 Email</a>')
    
    if DESENVOLVEDOR.get('linkedin'):
        links.append(f'<a href="{DESENVOLVEDOR["linkedin"]}" class="footer-link" target="_blank">💼 LinkedIn</a>')
    
    if DESENVOLVEDOR.get('github'):
        links.append(f'<a href="{DESENVOLVEDOR["github"]}" class="footer-link" target="_blank">💻 GitHub</a>')
    
    if DESENVOLVEDOR.get('portfolio'):
        links.append(f'<a href="{DESENVOLVEDOR["portfolio"]}" class="footer-link" target="_blank">🌐 Portfolio</a>')
    
    links_html = "".join(links)
    
    st.markdown(f"""
        <div class='footer-container'>
            <div class='footer-title'>
                👨‍💻 Desenvolvido por {DESENVOLVEDOR['nome']}
            </div>
            <div class='footer-info'>
                {DESENVOLVEDOR.get('cargo', 'Desenvolvedor')}
            </div>
            <div class='footer-links'>
                {links_html}
            </div>
            <div class='footer-copyright'>
                © {datetime.now().year} {EMPRESA['nome']} | Sistema de Gestão v{VERSAO} ({DATA_VERSAO})
                {f' | Página: {pagina}' if pagina else ''}
            </div>
        </div>
    """, unsafe_allow_html=True)


def exibir_header_customizado(titulo: str, subtitulo: str = "", icone: str = "📊"):
    st.markdown(f"""
        <style>
        .custom-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .custom-header h1 {{
            color: white;
            font-size: 2.5rem;
            margin: 0;
            text-align: center;
        }}
        .custom-header p {{
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            margin: 10px 0 0 0;
            text-align: center;
        }}
        </style>
        
        <div class='custom-header'>
            <h1>{icone} {titulo}</h1>
            {f'<p>{subtitulo}</p>' if subtitulo else ''}
        </div>
    """, unsafe_allow_html=True)


def exibir_badge_personalizado(texto: str, cor: str = "#3498db", icone: str = ""):
    st.markdown(f"""
        <span style='
            background-color: {cor};
            color: white;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.85rem;
            font-weight: bold;
            display: inline-block;
            margin-right: 5px;
        '>
            {icone} {texto}
        </span>
    """, unsafe_allow_html=True)