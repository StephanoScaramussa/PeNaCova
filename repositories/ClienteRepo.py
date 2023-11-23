from typing import List
from models.Cliente import Cliente
from models.Usuario import Usuario
from util.Database import Database

class ClienteRepo:

    @classmethod
    def criarTabela(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            senha TEXT NOT NULL,
            token TEXT,
            admin BOOLEAN NOT NULL DEFAULT 0,
            UNIQUE (email),
            UNIQUE (cpf) )
        """
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        tableCreated = cursor.execute(sql).rowcount > 0
        conexao.commit()
        conexao.close()
        return tableCreated
    
    @classmethod
    def criarUsuarioAdmin(cls) -> bool:
        sql = "INSERT OR IGNORE INTO cliente (nome, cpf, email, telefone, senha, admin) VALUES (?, ?, ?, ?, ?, ?)"
        # hash da senha 123456
        hash_senha = "$2b$12$WU9pnIyBUZOJHN7hgkhWtew8hI0Keiobr8idjIxYDwCyiSb5zh0iq"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, ("Alemao", "16375916755", "alemao@email.com", "28999928218", hash_senha, True)
        )
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def inserir(cls, cliente: Cliente) -> Cliente:
        sql = "INSERT INTO cliente (nome, cpf, email, telefone, senha) VALUES (?, ?, ?, ?, ?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(
            sql, (cliente.nome, cliente.cpf, cliente.email, cliente.telefone, cliente.senha)
        )
        if resultado.rowcount > 0:
            cliente.id = resultado.lastrowid
        conexao.commit()
        conexao.close()
        return cliente
    
    @classmethod
    def inserirToken(cls, token: str, idUsuario: int) -> bool:
        sql = "UPDATE cliente SET token=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, idUsuario))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False

    @classmethod
    def alterar(cls, cliente: Cliente) -> Cliente:
        sql = "UPDATE cliente SET nome=?, cpf=?, email=?, telefone=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (cliente.nome, cliente.cpf, cliente.email, cliente.telefone, cliente.id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return cliente
        else:
            conexao.close()
            return None
        
    @classmethod
    def alterarSenha(cls, id: int, senha: str) -> bool:
        sql = "UPDATE cliente SET senha=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (senha, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
    
    @classmethod
    def alterarNome(cls, id: int, nome: str) -> bool:
        sql = "UPDATE cliente SET nome=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (nome, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def alterarCPF(cls, id: int, cpf: str) -> bool:
        sql = "UPDATE cliente SET cpf=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (cpf, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
    
    @classmethod
    def alterarEmail(cls, id: int, email: str) -> bool:
        sql = "UPDATE cliente SET email=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def alterarTelefone(cls, id: int, telefone: str) -> bool:
        sql = "UPDATE cliente SET telefone=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (telefone, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def alterarToken(cls, email: str, token: str) -> bool:
        sql = "UPDATE cliente SET token=? WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (token, email))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def alterarAdmin(cls, id: int, admin: bool) -> bool:
        sql = "UPDATE cliente SET admin=? WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (admin, id))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def emailExiste(cls, email: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM cliente WHERE email=?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()        
        return bool(resultado[0])
    
    @classmethod
    def cpfExiste(cls, cpf: str) -> bool:
        sql = "SELECT EXISTS (SELECT 1 FROM cliente WHERE cpf=?)"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (cpf,)).fetchone()        
        return bool(resultado[0])
    
    @classmethod
    def obterSenhaDeEmail(cls, email: str) -> str | None:
        sql = "SELECT senha FROM cliente WHERE email=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (email,)).fetchone()
        if resultado:
            return str(resultado[0])
        else:
            return None
        
    @classmethod
    def excluir(cls, id: int) -> bool:
        sql = "DELETE FROM cliente WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,))
        if resultado.rowcount > 0:
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.close()
            return False
        
    @classmethod
    def obterTodos(cls) -> List[Cliente]:
        sql = "SELECT id, nome, cpf, email, telefone, admin FROM cliente ORDER BY nome"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql).fetchall()
        objetos = [
            Cliente(
                id=x[0],
                nome=x[1],
                cpf=x[2],
                email=x[3],
                telefone=x[4],
                admin=x[5]
            )
            for x in resultado
        ]
        return objetos
    
    @classmethod
    def obterPagina(cls, pagina: int, tamanhoPagina: int) -> List[Cliente]:
        inicio = (pagina - 1) * tamanhoPagina
        sql = "SELECT cliente.id, cliente.nome, cliente.cpf, cliente.email, cliente.telefone, cliente.admin FROM cliente ORDER BY cliente.nome LIMIT ?, ?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (inicio, tamanhoPagina)).fetchall()
        objetos = [
            Cliente(
                id=x[0],
                nome=x[1],
                cpf=x[2],
                email=x[3],
                telefone=x[4],
                admin=x[5],
            )
            for x in resultado
        ]
        return objetos
    
    @classmethod
    def obterQtdePaginas(cls, tamanhoPagina: int) -> int:
        sql = "SELECT CEIL(CAST((SELECT COUNT(*) FROM cliente) AS FLOAT) / ?) AS qtdePaginas"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (tamanhoPagina,)).fetchone()
        return int(resultado[0])
    
    @classmethod
    def obterPorId(cls, id: int) -> Cliente | None:
        sql = "SELECT id, nome, cpf, email, telefone, admin FROM cliente WHERE id=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        resultado = cursor.execute(sql, (id,)).fetchone()
        if (resultado):
            objeto = Cliente(
                id=resultado[0],
                nome=resultado[1],
                cpf=resultado[2],
                email=resultado[3],
                telefone=resultado[4],
                admin=resultado[5],
            )
            return objeto
        else: 
            return None
        
    # @classmethod
    # def obterPorId(cls, id: int) -> Aluno | None:
    #     sql = "SELECT aluno.id, aluno.nome, aluno.email, aluno.admin, aluno.aprovado, aluno.idProjeto, projeto.nome AS nomeProjeto FROM aluno INNER JOIN projeto ON aluno.idProjeto = projeto.id WHERE aluno.id=?"
    #     conexao = Database.criarConexao()
    #     cursor = conexao.cursor()
    #     resultado = cursor.execute(sql, (id,)).fetchone()
    #     if (resultado):
    #         objeto = Aluno(
    #             id=resultado[0],
    #             nome=resultado[1],
    #             email=resultado[2],
    #             admin=resultado[3],
    #             aprovado=resultado[4],
    #             idProjeto=resultado[5],
    #             nomeProjeto=resultado[6],
    #         )
    #         return objeto
    #     else: 
    #         return None

    @classmethod
    def obterClientePorToken(cls, token: str) -> Usuario:
        sql = "SELECT id, nome, email, admin FROM cliente WHERE token=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (token,)).fetchone()
        if resultado:
            objeto = Usuario(*resultado)
            return objeto
        else:
            return None
        
    @classmethod
    def obterClientePorCPF(cls, cpf: str) -> Cliente:
        sql = "SELECT nome, cpf, email, telefone, token, admin FROM cliente WHERE cpf=?"
        conexao = Database.criarConexao()
        cursor = conexao.cursor()
        # quando se executa fechone em um cursor sem resultado, ele retorna None
        resultado = cursor.execute(sql, (cpf,)).fetchone()
        if resultado:
            objeto = Cliente(*resultado)
            return objeto
        else:
            return None
