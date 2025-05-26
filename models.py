import sqlite3

class Usuario:
    @staticmethod
    def cadastrar(email, senha):
        """
        Cadastra um novo usuário com email e senha.
        Retorna True se cadastro for bem-sucedido, False se o email já estiver cadastrado.
        """
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (email, senha) VALUES (?, ?)",
                (email.strip().lower(), senha)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Email já cadastrado
            return False
        finally:
            conn.close()

    @staticmethod
    def autenticar(email, senha):
        """
        Autentica um usuário verificando email e senha.
        Retorna True se credenciais estiverem corretas, False caso contrário.
        """
        conn = sqlite3.connect("tarefas.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email.strip().lower(), senha)
        )
        usuario = cursor.fetchone()
        conn.close()
        
        return usuario is not None


class Tarefa:
    def __init__(self, titulo, descricao, categoria, prioridade, data, hora, concluida):
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.prioridade = prioridade
        self.data = data
        self.hora = hora
        self.concluida = concluida
