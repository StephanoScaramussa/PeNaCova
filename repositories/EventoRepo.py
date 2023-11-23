from typing import List
from models.Evento import Evento
from util.Database import Database

class EventoRepo:
    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS evento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            imagem TEXT NOT NULL,
            descricao TEXT NOT NULL
            )
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def inserir(cls, evento: Evento) -> Evento:
        sql = "INSERT INTO evento (titulo, imagem, descricao) VALUES (?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (evento.titulo, evento.imagem, evento.descricao)
        )
        if resultado.rowcount > 0:
            evento.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return evento
    
    @classmethod
    def alterar(cls, evento: Evento) -> Evento:
        sql = "UPDATE evento SET titulo=?, imagem=?, descricao=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (evento.titulo, evento.imagem, evento.descricao, evento.id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return evento
        else:
            conexao.close()
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM evento WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, ))
        if (resultado.rowcount > 0):
            conexao.commit()
            conexao.close()
            return True
        else: 
            conexao.close()
            return False
        
    @classmethod
    def obterTodosParaSelect(cls) -> List[Evento]:
        sql = "SELECT id, titulo, imagem, descricao FROM evento ORDER BY titulo"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [Evento(id=x[0], titulo=x[1]) for x in resultado]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Evento]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT id, titulo, imagem, descricao FROM evento ORDER BY titulo LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [Evento(*x) for x in resultado]
        return objetos
    
    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM evento) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina, )).fetchone()
        return int(resultado[0])
    
    @classmethod
    def obterPorId(cls, id: int) -> Evento:
        sql = "SELECT id, titulo, imagem, descricao FROM evento WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id, )).fetchone()
        objeto = Evento(*resultado)
        return objeto