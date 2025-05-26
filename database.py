import sqlite3

def criar_banco():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    
    # Criar tabela de usuários
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    """)
    
    # Criar tabela de tarefas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        titulo TEXT NOT NULL,
        descricao TEXT,
        categoria TEXT,
        prioridade TEXT,
        data TEXT,
        hora TEXT,
        concluida INTEGER,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    )
    """)
    
    conn.commit()
    conn.close()

def adicionar_tarefa(usuario_email, titulo, descricao, categoria, prioridade, data, hora, concluida):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    
    # Obter o id do usuário
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (usuario_email,))
    usuario = cursor.fetchone()
    if usuario is None:
        conn.close()
        raise ValueError("Usuário não encontrado no banco de dados.")
    usuario_id = usuario[0]
    
    cursor.execute("""
    INSERT INTO tarefas (usuario_id, titulo, descricao, categoria, prioridade, data, hora, concluida)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (usuario_id, titulo, descricao, categoria, prioridade, data, hora, int(concluida)))
    
    conn.commit()
    conn.close()

def obter_tarefas(usuario_email):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    
    # Obter o id do usuário
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (usuario_email,))
    usuario = cursor.fetchone()
    if usuario is None:
        conn.close()
        return []  # Retorna lista vazia se usuário não for encontrado
    usuario_id = usuario[0]
    
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id = ?", (usuario_id,))
    tarefas = cursor.fetchall()
    
    conn.close()
    return tarefas

def atualizar_tarefa(tarefa_id, usuario_email, titulo, descricao, categoria, prioridade, data, concluida):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    UPDATE tarefas
    SET titulo = ?, descricao = ?, categoria = ?, prioridade = ?, data = ?, concluida = ?
    WHERE id = ?
    """, (titulo, descricao, categoria, prioridade, data, int(concluida), tarefa_id))
    
    conn.commit()
    conn.close()

def deletar_tarefa(tarefa_id, usuario_email):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    
    conn.commit()
    conn.close()

