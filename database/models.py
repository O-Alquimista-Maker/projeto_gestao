"""
Definição dos schemas das tabelas do banco de dados
"""

SCHEMA_ANOTACOES = """
CREATE TABLE IF NOT EXISTS anotacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    conteudo TEXT,
    categoria TEXT DEFAULT 'Geral',
    tags TEXT,
    prioridade TEXT DEFAULT 'média',
    arquivada INTEGER DEFAULT 0,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_modificacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

SCHEMA_OCORRENCIAS = """
CREATE TABLE IF NOT EXISTS ocorrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    severidade TEXT DEFAULT 'média',
    status TEXT DEFAULT 'aberta',
    data_ocorrencia TIMESTAMP,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responsavel TEXT,
    solucao TEXT,
    anexos TEXT
)
"""

SCHEMA_ATAS = """
CREATE TABLE IF NOT EXISTS atas_reuniao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    data_reuniao DATE NOT NULL,
    horario_inicio TIME,
    horario_fim TIME,
    participantes TEXT,
    pauta TEXT,
    discussoes TEXT,
    decisoes TEXT,
    acoes TEXT,
    proxima_reuniao DATE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

SCHEMA_TAGS = """
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    cor TEXT DEFAULT '#3498db',
    tipo TEXT DEFAULT 'anotacao'
)
"""

ALL_SCHEMAS = [
    SCHEMA_ANOTACOES,
    SCHEMA_OCORRENCIAS,
    SCHEMA_ATAS,
    SCHEMA_TAGS
]