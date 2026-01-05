"""
Gerenciador do banco de dados SQLite
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from .models import ALL_SCHEMAS


class DatabaseManager:
    def __init__(self, db_path: str = "dados_gestao.db"):
        """Inicializa o gerenciador do banco de dados"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Retorna uma conexão com o banco"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        return conn
    
    def init_database(self):
        """Cria as tabelas se não existirem"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for schema in ALL_SCHEMAS:
            cursor.execute(schema)
        
        conn.commit()
        conn.close()
    
    # ==================== ANOTAÇÕES ====================
    
    def criar_anotacao(self, titulo: str, conteudo: str, categoria: str = "Geral", 
                       tags: List[str] = None, prioridade: str = "média") -> int:
        """Cria uma nova anotação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        tags_json = json.dumps(tags) if tags else json.dumps([])
        
        cursor.execute("""
            INSERT INTO anotacoes (titulo, conteudo, categoria, tags, prioridade)
            VALUES (?, ?, ?, ?, ?)
        """, (titulo, conteudo, categoria, tags_json, prioridade))
        
        anotacao_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return anotacao_id
    
    def listar_anotacoes(self, arquivada: bool = False, categoria: str = None) -> List[Dict]:
        """Lista todas as anotações"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM anotacoes WHERE arquivada = ?"
        params = [1 if arquivada else 0]
        
        if categoria and categoria != "Todas":
            query += " AND categoria = ?"
            params.append(categoria)
        
        query += " ORDER BY data_modificacao DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        anotacoes = []
        for row in rows:
            anotacao = dict(row)
            anotacao['tags'] = json.loads(anotacao['tags']) if anotacao['tags'] else []
            anotacoes.append(anotacao)
        
        return anotacoes
    
    def buscar_anotacao(self, anotacao_id: int) -> Optional[Dict]:
        """Busca uma anotação específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM anotacoes WHERE id = ?", (anotacao_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            anotacao = dict(row)
            anotacao['tags'] = json.loads(anotacao['tags']) if anotacao['tags'] else []
            return anotacao
        return None
    
    def atualizar_anotacao(self, anotacao_id: int, titulo: str = None, 
                          conteudo: str = None, categoria: str = None,
                          tags: List[str] = None, prioridade: str = None):
        """Atualiza uma anotação existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if titulo is not None:
            updates.append("titulo = ?")
            params.append(titulo)
        if conteudo is not None:
            updates.append("conteudo = ?")
            params.append(conteudo)
        if categoria is not None:
            updates.append("categoria = ?")
            params.append(categoria)
        if tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(tags))
        if prioridade is not None:
            updates.append("prioridade = ?")
            params.append(prioridade)
        
        if updates:
            updates.append("data_modificacao = CURRENT_TIMESTAMP")
            query = f"UPDATE anotacoes SET {', '.join(updates)} WHERE id = ?"
            params.append(anotacao_id)
            
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def deletar_anotacao(self, anotacao_id: int):
        """Deleta uma anotação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM anotacoes WHERE id = ?", (anotacao_id,))
        conn.commit()
        conn.close()
    
    def arquivar_anotacao(self, anotacao_id: int, arquivar: bool = True):
        """Arquiva ou desarquiva uma anotação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE anotacoes SET arquivada = ? WHERE id = ?", 
                      (1 if arquivar else 0, anotacao_id))
        conn.commit()
        conn.close()
    
    def buscar_anotacoes(self, termo: str) -> List[Dict]:
        """Busca anotações por termo no título ou conteúdo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM anotacoes 
            WHERE (titulo LIKE ? OR conteudo LIKE ?) AND arquivada = 0
            ORDER BY data_modificacao DESC
        """, (f"%{termo}%", f"%{termo}%"))
        
        rows = cursor.fetchall()
        conn.close()
        
        anotacoes = []
        for row in rows:
            anotacao = dict(row)
            anotacao['tags'] = json.loads(anotacao['tags']) if anotacao['tags'] else []
            anotacoes.append(anotacao)
        
        return anotacoes
    
    def obter_categorias(self) -> List[str]:
        """Retorna lista de categorias únicas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT categoria FROM anotacoes ORDER BY categoria")
        categorias = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categorias
    
    # ==================== OCORRÊNCIAS ====================
    
    def criar_ocorrencia(self, tipo: str, descricao: str, severidade: str = "média",
                        data_ocorrencia: str = None, responsavel: str = None,
                        solucao: str = None) -> int:
        """Cria uma nova ocorrência"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if not data_ocorrencia:
            data_ocorrencia = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO ocorrencias (tipo, descricao, severidade, data_ocorrencia, responsavel, solucao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tipo, descricao, severidade, data_ocorrencia, responsavel, solucao))
        
        ocorrencia_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return ocorrencia_id
    
    def listar_ocorrencias(self, status: str = None, severidade: str = None, 
                          tipo: str = None) -> List[Dict]:
        """Lista todas as ocorrências com filtros opcionais"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM ocorrencias WHERE 1=1"
        params = []
        
        if status and status != "Todos":
            query += " AND status = ?"
            params.append(status.lower())
        
        if severidade and severidade != "Todas":
            query += " AND severidade = ?"
            params.append(severidade.lower())
        
        if tipo and tipo != "Todos":
            query += " AND tipo = ?"
            params.append(tipo)
        
        query += " ORDER BY data_ocorrencia DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def buscar_ocorrencia(self, ocorrencia_id: int) -> Optional[Dict]:
        """Busca uma ocorrência específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ocorrencias WHERE id = ?", (ocorrencia_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def atualizar_ocorrencia(self, ocorrencia_id: int, tipo: str = None,
                            descricao: str = None, severidade: str = None,
                            status: str = None, responsavel: str = None,
                            solucao: str = None):
        """Atualiza uma ocorrência existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if tipo is not None:
            updates.append("tipo = ?")
            params.append(tipo)
        if descricao is not None:
            updates.append("descricao = ?")
            params.append(descricao)
        if severidade is not None:
            updates.append("severidade = ?")
            params.append(severidade)
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if responsavel is not None:
            updates.append("responsavel = ?")
            params.append(responsavel)
        if solucao is not None:
            updates.append("solucao = ?")
            params.append(solucao)
        
        if updates:
            query = f"UPDATE ocorrencias SET {', '.join(updates)} WHERE id = ?"
            params.append(ocorrencia_id)
            
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def deletar_ocorrencia(self, ocorrencia_id: int):
        """Deleta uma ocorrência"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ocorrencias WHERE id = ?", (ocorrencia_id,))
        conn.commit()
        conn.close()
    
    def obter_ocorrencias_por_status(self) -> Dict[str, int]:
        """Retorna contagem de ocorrências por status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM ocorrencias 
            GROUP BY status
        """)
        
        resultado = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        return resultado
    
    def obter_ocorrencias_por_severidade(self) -> Dict[str, int]:
        """Retorna contagem de ocorrências por severidade"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT severidade, COUNT(*) as count 
            FROM ocorrencias 
            GROUP BY severidade
        """)
        
        resultado = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        return resultado
    
    def obter_ocorrencias_criticas_abertas(self) -> List[Dict]:
        """Retorna ocorrências críticas que ainda estão abertas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM ocorrencias 
            WHERE severidade = 'crítica' AND status IN ('aberta', 'em análise')
            ORDER BY data_ocorrencia DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ==================== ATAS DE REUNIÃO ====================
    
    def criar_ata(self, titulo: str, data_reuniao: str, horario_inicio: str = None,
                  horario_fim: str = None, participantes: List[str] = None,
                  pauta: str = None, discussoes: str = None, decisoes: str = None,
                  acoes: List[Dict] = None, proxima_reuniao: str = None) -> int:
        """Cria uma nova ata de reunião"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        participantes_json = json.dumps(participantes) if participantes else json.dumps([])
        acoes_json = json.dumps(acoes) if acoes else json.dumps([])
        
        cursor.execute("""
            INSERT INTO atas_reuniao (titulo, data_reuniao, horario_inicio, horario_fim,
                                     participantes, pauta, discussoes, decisoes, acoes, proxima_reuniao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titulo, data_reuniao, horario_inicio, horario_fim, participantes_json,
              pauta, discussoes, decisoes, acoes_json, proxima_reuniao))
        
        ata_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return ata_id
    
    def listar_atas(self, limite: int = None) -> List[Dict]:
        """Lista todas as atas de reunião"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM atas_reuniao ORDER BY data_reuniao DESC"
        
        if limite:
            query += f" LIMIT {limite}"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        atas = []
        for row in rows:
            ata = dict(row)
            ata['participantes'] = json.loads(ata['participantes']) if ata['participantes'] else []
            ata['acoes'] = json.loads(ata['acoes']) if ata['acoes'] else []
            atas.append(ata)
        
        return atas
    
    def buscar_ata(self, ata_id: int) -> Optional[Dict]:
        """Busca uma ata específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM atas_reuniao WHERE id = ?", (ata_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            ata = dict(row)
            ata['participantes'] = json.loads(ata['participantes']) if ata['participantes'] else []
            ata['acoes'] = json.loads(ata['acoes']) if ata['acoes'] else []
            return ata
        return None
    
    def atualizar_ata(self, ata_id: int, titulo: str = None, data_reuniao: str = None,
                     horario_inicio: str = None, horario_fim: str = None,
                     participantes: List[str] = None, pauta: str = None,
                     discussoes: str = None, decisoes: str = None,
                     acoes: List[Dict] = None, proxima_reuniao: str = None):
        """Atualiza uma ata existente"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if titulo is not None:
            updates.append("titulo = ?")
            params.append(titulo)
        if data_reuniao is not None:
            updates.append("data_reuniao = ?")
            params.append(data_reuniao)
        if horario_inicio is not None:
            updates.append("horario_inicio = ?")
            params.append(horario_inicio)
        if horario_fim is not None:
            updates.append("horario_fim = ?")
            params.append(horario_fim)
        if participantes is not None:
            updates.append("participantes = ?")
            params.append(json.dumps(participantes))
        if pauta is not None:
            updates.append("pauta = ?")
            params.append(pauta)
        if discussoes is not None:
            updates.append("discussoes = ?")
            params.append(discussoes)
        if decisoes is not None:
            updates.append("decisoes = ?")
            params.append(decisoes)
        if acoes is not None:
            updates.append("acoes = ?")
            params.append(json.dumps(acoes))
        if proxima_reuniao is not None:
            updates.append("proxima_reuniao = ?")
            params.append(proxima_reuniao)
        
        if updates:
            query = f"UPDATE atas_reuniao SET {', '.join(updates)} WHERE id = ?"
            params.append(ata_id)
            
            cursor.execute(query, params)
            conn.commit()
        
        conn.close()
    
    def deletar_ata(self, ata_id: int):
        """Deleta uma ata de reunião"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM atas_reuniao WHERE id = ?", (ata_id,))
        conn.commit()
        conn.close()
    
    def buscar_atas_por_periodo(self, data_inicio: str, data_fim: str) -> List[Dict]:
        """Busca atas em um período específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM atas_reuniao 
            WHERE data_reuniao BETWEEN ? AND ?
            ORDER BY data_reuniao DESC
        """, (data_inicio, data_fim))
        
        rows = cursor.fetchall()
        conn.close()
        
        atas = []
        for row in rows:
            ata = dict(row)
            ata['participantes'] = json.loads(ata['participantes']) if ata['participantes'] else []
            ata['acoes'] = json.loads(ata['acoes']) if ata['acoes'] else []
            atas.append(ata)
        
        return atas
    
    def obter_acoes_pendentes(self) -> List[Dict]:
        """Retorna todas as ações pendentes de todas as atas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, titulo, acoes, data_reuniao FROM atas_reuniao")
        rows = cursor.fetchall()
        conn.close()
        
        acoes_pendentes = []
        for row in rows:
            ata_id = row[0]
            titulo_ata = row[1]
            acoes_json = row[2]
            data_reuniao = row[3]
            
            if acoes_json:
                acoes = json.loads(acoes_json)
                for acao in acoes:
                    if not acao.get('concluida', False):
                        acoes_pendentes.append({
                            'ata_id': ata_id,
                            'titulo_ata': titulo_ata,
                            'data_reuniao': data_reuniao,
                            'acao': acao.get('descricao', ''),
                            'responsavel': acao.get('responsavel', ''),
                            'prazo': acao.get('prazo', '')
                        })
        
        return acoes_pendentes
    
    
    # ==================== ESTATÍSTICAS ====================
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais do sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Anotações
        cursor.execute("SELECT COUNT(*) FROM anotacoes WHERE arquivada = 0")
        total_anotacoes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM anotacoes WHERE arquivada = 1")
        anotacoes_arquivadas = cursor.fetchone()[0]
        
        # Ocorrências
        cursor.execute("SELECT COUNT(*) FROM ocorrencias WHERE status != 'fechada'")
        ocorrencias_abertas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ocorrencias")
        total_ocorrencias = cursor.fetchone()[0]
        
        # Atas
        cursor.execute("SELECT COUNT(*) FROM atas_reuniao")
        total_atas = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_anotacoes': total_anotacoes,
            'anotacoes_arquivadas': anotacoes_arquivadas,
            'ocorrencias_abertas': ocorrencias_abertas,
            'total_ocorrencias': total_ocorrencias,
            'total_atas': total_atas
        }