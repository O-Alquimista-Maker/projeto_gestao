# 📊 Sistema de Gestão Integrado

Sistema completo de gerenciamento de **anotações**, **ocorrências** e **atas de reunião** desenvolvido com Streamlit e SQLite.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🚀 Funcionalidades

### 📝 Módulo de Anotações
- ✅ CRUD completo de anotações
- ✅ Sistema de tags e categorias
- ✅ Prioridades (Baixa, Média, Alta)
- ✅ Busca avançada
- ✅ Arquivamento de anotações
- ✅ Suporte a Markdown

### 🚨 Módulo de Ocorrências
- ✅ Registro de incidentes e problemas
- ✅ Níveis de severidade (Baixa, Média, Alta, Crítica)
- ✅ Status personalizados
- ✅ Dashboard com gráficos interativos
- ✅ Alertas para ocorrências críticas
- ✅ Timeline de ocorrências

### 📋 Módulo de Atas de Reunião
- ✅ Documentação completa de reuniões
- ✅ Gerenciamento de participantes
- ✅ Plano de ação com responsáveis e prazos
- ✅ Acompanhamento de ações pendentes
- ✅ Indicadores de status (atrasada, hoje, próxima)
- ✅ Relatórios estatísticos

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework web
- **SQLite** - Banco de dados local
- **Plotly** - Gráficos interativos
- **Pandas** - Manipulação de dados

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/projeto-gestao.git
cd projeto-gestao
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o sistema
Edite o arquivo `config.py` com suas informações:
```python
EMPRESA = {
    'nome': 'Sua Empresa',
    'logo_url': 'URL_DO_SEU_LOGO',
    # ...
}

DESENVOLVEDOR = {
    'nome': 'Seu Nome',
    # ...
}
```

### 5. Execute a aplicação
```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto
```
projeto_gestao/
├── app.py                      # Aplicação principal
├── config.py                   # Configurações do sistema
├── requirements.txt            # Dependências
├── database/
│   ├── __init__.py
│   ├── db_manager.py          # Gerenciador do banco
│   └── models.py              # Esquemas das tabelas
├── pages/
│   ├── 1_📝_Anotacoes.py
│   ├── 2_🚨_Ocorrencias.py
│   └── 3_📋_Atas_Reuniao.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py             # Funções auxiliares
│   └── components.py          # Componentes visuais
└── assets/
    └── logo.png               # Logo da empresa
```

## 🎨 Personalização

O sistema oferece personalização completa através do arquivo `config.py`:

- **Logo da empresa** na sidebar
- **Informações da empresa**
- **Assinatura do desenvolvedor** no rodapé
- **Cores e tema** personalizados
- **Versão do sistema**

## 📊 Dashboard

O dashboard principal oferece:
- Métricas em tempo real
- Gráficos de distribuição
- Timeline de atividades
- Ações rápidas
- Atividades recentes

## 🔒 Banco de Dados

O sistema utiliza SQLite como banco de dados local, criando automaticamente o arquivo `dados_gestao.db` na primeira execução.

**Tabelas:**
- `anotacoes` - Armazena anotações
- `ocorrencias` - Registra ocorrências
- `atas_reuniao` - Documenta reuniões
- `tags` - Sistema de tags

## 🚀 Deploy

### Streamlit Cloud (Recomendado)

1. Faça push do projeto para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Configure e faça deploy!

### Deploy Manual

O sistema pode ser deployado em qualquer servidor que suporte Python e Streamlit.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Desenvolvedor

**Seu Nome**
- 📧 Email: seuemail@exemplo.com
- 💼 LinkedIn: [seu-perfil](https://linkedin.com/in/seu-perfil)
- 💻 GitHub: [seu-usuario](https://github.com/seu-usuario)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## 📸 Screenshots

_Adicione screenshots do sistema aqui_

## 🔄 Versão

**v1.0.0** - 05/01/2026
- ✅ Lançamento inicial
- ✅ Módulos de Anotações, Ocorrências e Atas
- ✅ Dashboard interativo
- ✅ Personalização completa

---

⭐ Se este projeto foi útil, considere dar uma estrela!