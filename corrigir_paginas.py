import re

paginas = [
    'pages/1_📝_Anotacoes.py',
    'pages/2_🚨_Ocorrencias.py', 
    'pages/3_📋_Atas_Reuniao.py'
]

for pagina in paginas:
    with open(pagina, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Adicionar imports se não existirem
    if 'from utils.components' not in conteudo:
        conteudo = conteudo.replace(
            'import streamlit as st',
            '''import streamlit as st
from utils.components import exibir_logo_sidebar, exibir_assinatura_footer
from auth import login_simples, exibir_info_usuario'''
        )
    
    # Adicionar autenticação após st.set_page_config
    if 'if not login_simples():' not in conteudo:
        conteudo = conteudo.replace(
            'layout="wide"\n)',
            'layout="wide"\n)\n\nif not login_simples():\n    st.stop()'
        )
    
    # Adicionar logo e info após título
    if 'exibir_logo_sidebar()' not in conteudo:
        conteudo = conteudo.replace(
            'st.markdown("---")',
            '''exibir_logo_sidebar()
exibir_info_usuario()

st.markdown("---")''',
            1
        )
    
    # Adicionar footer no final
    if 'exibir_assinatura_footer' not in conteudo:
        nome_pagina = pagina.split('_')[1].replace('.py', '')
        conteudo += f'\n\nexibir_assinatura_footer(pagina="{nome_pagina}")'
    
    with open(pagina, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"✅ {pagina} corrigido!")

print("\n🎉 Todas as páginas foram corrigidas!")