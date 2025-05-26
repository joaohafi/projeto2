import streamlit as st
from datetime import datetime
from models import Usuario, Tarefa
from database import (
    criar_banco,
    adicionar_tarefa,
    obter_tarefas,
    atualizar_tarefa,
    deletar_tarefa,
)
from utils import exportar_tarefas_csv, mostrar_imagem_de_fundo

# Inicializar banco de dados (cria arquivo e tabelas se não existirem)
criar_banco()

# Definir cores modernas para prioridades usando nuances mais suaves e elegantes
COR_PRIORIDADE = {
    "Alta": "rgba(255, 77, 79, 0.15)",  # vermelho suave
    "Média": "rgba(255, 193, 7, 0.15)",  # amarelo suave
    "Baixa": "rgba(40, 167, 69, 0.15)",  # verde suave
}

# Ícones grandes e modernos para prioridade e categoria
ICONE_PRIORIDADE = {
    "Alta": "🔥",
    "Média": "⚡",
    "Baixa": "🌿",
}

ICONE_CATEGORIA = {
    "Treino": "🏋️",
    "Dieta": "🥗",
    "Compromisso": "📆",
}

CATEGORIAS = list(ICONE_CATEGORIA.keys())
PRIORIDADES = list(ICONE_PRIORIDADE.keys())

# Estado da sessão para usuário logado e edição
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "editar_tarefa_id" not in st.session_state:
    st.session_state.editar_tarefa_id = None

# Estilo CSS moderno com fontes Google Fonts, gradientes, sombras e animações
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Roboto&display=swap');

body {
    font-family: 'Montserrat', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #222;
    margin: 0 !important;
    padding: 0 !important;
}

h1, h2, h3, h4 {
    color: #f7f7f7;
}

.stButton>button {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 30px;
    padding: 10px 25px;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.5);
}

.stButton>button:hover {
    background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    box-shadow: 0 6px 14px rgba(118, 75, 162, 0.7);
    transform: translateY(-2px);
}

.custom-header {
    font-size: 2.6rem;
    font-weight: 800;
    margin-bottom: 1.8rem;
    text-align: center;
    color: #fff;
    text-shadow: 0 0 12px rgba(255, 255, 255, 0.9);
    user-select: none;
    letter-spacing: 1.2px;
}

.card-tarefa {
    background: #fff;
    border-radius: 20px;
    padding: 20px 28px;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    transition: box-shadow 0.3s ease, transform 0.25s ease;
    border-left: 8px solid;
}

.card-tarefa:hover {
    box-shadow: 0 18px 45px rgba(0,0,0,0.25);
    transform: translateY(-6px);
}

.titulo-tarefa {
    font-size: 1.5rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 14px;
    color: #222;
}

.titulo-tarefa.concluida {
    text-decoration: line-through;
    color: #999;
    font-style: italic;
}

.detalhes-tarefa {
    font-size: 1rem;
    margin: 6px 0;
    color: #444;
    line-height: 1.4;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #5a45d6 0%, #333bbb 100%);
    color: white !important;
    border-radius: 0 20px 20px 0;
    padding: 1.3rem 1.5rem;
    font-weight: 600;
    font-size: 1.1rem;
}

.stRadio > div {
    color: white;
    font-weight: 600;
}

.stTextInput > div > input, .stTextArea > div > textarea {
    border-radius: 14px;
    border: 2px solid #764ba2;
    padding: 12px;
    font-family: 'Roboto', sans-serif;
    font-size: 1.1rem;
    transition: box-shadow 0.3s ease;
}

.stTextInput > div > input:focus, .stTextArea > div > textarea:focus {
    outline: none;
    box-shadow: 0 0 12px #764ba2;
    border-color: #667eea;
}

select, option {
    border-radius: 12px;
    padding: 10px;
    font-weight: 600;
    font-size: 1rem;
}

.stCheckbox > div {
    color: #f0f0f0;
    font-weight: 700;
    font-size: 1rem;
}

.download-button button {
    background: rgba(118, 75, 162, 0.95) !important;
    border-radius: 36px !important;
    padding: 14px 36px !important;
    font-weight: 800 !important;
    font-size: 1.15rem !important;
    color: #fff !important;
    box-shadow: 0 8px 20px rgba(118, 75, 162, 0.65) !important;
    transition: background 0.3s ease !important;
}

.download-button button:hover {
    background: rgba(102,126,234, 0.95) !important;
    box-shadow: 0 12px 28px rgba(102,126,234, 0.85) !important;
    transform: translateY(-3px) !important;
}

button[title="Marcar como concluída"], button[title="Marcar como pendente"], button[title="Editar tarefa"], button[title="Excluir tarefa"] {
    border-radius: 24px !important;
    padding: 8px 18px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    box-shadow: 0 5px 15px rgba(50,50,93,.11), 0 10px 20px rgba(50,50,93,.08);
    transition: background-color 0.3s ease, transform 0.2s ease !important;
}

button[title="Marcar como concluída"]:hover, button[title="Marcar como pendente"]:hover {
    background-color: #28a745 !important;
    color: white !important;
    transform: translateY(-1.5px) !important;
    box-shadow: 0 8px 24px rgba(40,167,69,.5) !important;
}

button[title="Editar tarefa"]:hover {
    background-color: #ffc107 !important;
    color: black !important;
    transform: translateY(-1.5px) !important;
    box-shadow: 0 8px 24px rgba(255,193,7,.5) !important;
}

button[title="Excluir tarefa"]:hover {
    background-color: #dc3545 !important;
    color: white !important;
    transform: translateY(-1.5px) !important;
    box-shadow: 0 8px 24px rgba(220,53,69,.5) !important;
}

.form-container {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    padding: 1.3rem 2rem 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
}

.footer {
    text-align: center;
    margin-top: 3rem;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.75);
    user-select: none;
}

"""

# Aplica o CSS
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# Mostrar imagem de fundo (se tiver implementada)
mostrar_imagem_de_fundo()

# Cabeçalho principal com emoji e estilo
st.markdown(
    '<div class="custom-header">📋 Plataforma de Tarefas Avançada para Atletas</div>',
    unsafe_allow_html=True,
)

def tela_login_cadastro():
    """
    Tela para login e cadastro de usuários com feedback visual moderno e centralizado.
    """
    st.header("Faça Login ou Cadastre-se")
    aba = st.radio("Escolha uma opção:", ["Login", "Cadastro"], horizontal=True)
    
    email = st.text_input("E-mail", key="email_input")
    senha = st.text_input("Senha", type="password", key="senha_input")

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if aba == "Cadastro":
            if st.button("Cadastrar", use_container_width=True):
                if not email.strip() or not senha:
                    st.error("Preencha e-mail e senha para cadastro.")
                elif Usuario.cadastrar(email, senha):
                    st.success("Cadastro realizado com sucesso! Faça login para continuar.")
                    st.rerun()
                else:
                    st.error("Este e-mail já está cadastrado ou erro no cadastro.")
        else:
            if st.button("Login", use_container_width=True):
                if not email.strip() or not senha:
                    st.error("Preencha e-mail e senha para login.")
                elif Usuario.autenticar(email, senha):
                    st.session_state.usuario_logado = email.strip().lower()
                    st.success(f"Bem-vindo, {st.session_state.usuario_logado}!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos. Tente novamente.")

def carregar_tarefas_do_usuario():
    """
    Busca as tarefas do banco de dados e filtra pelo usuário logado.
    """
    if not st.session_state.usuario_logado:
        return []

    linhas = obter_tarefas(st.session_state.usuario_logado)
    tarefas = []
    for linha in linhas:
        (
            id,
            usuario_id,
            titulo,
            descricao,
            categoria,
            prioridade,
            data_str,
            hora_str,
            concluida_int,
        ) = linha
        data = datetime.strptime(data_str, "%Y-%m-%d")
        concluida = bool(concluida_int)
        tarefas.append(
            {
                "id": id,
                "titulo": titulo,
                "descricao": descricao,
                "categoria": categoria,
                "prioridade": prioridade,
                "data": data,
                "hora": hora_str,
                "concluida": concluida,
            }
        )
    return tarefas

def tela_gerenciamento_tarefas():
    """
    Tela principal após login:
    Exibe tarefas com layout super moderno, interativo e elegante.
    """
    st.sidebar.markdown(f"### 👤 Usuário: **{st.session_state.usuario_logado}**")
    if st.sidebar.button("Logout"):
        st.session_state.usuario_logado = None
        st.session_state.editar_tarefa_id = None
        st.rerun()

    # Seção adicionar nova tarefa estilizada
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    st.header("✍️ Adicionar Nova Tarefa")
    with st.form("form_tarefa", clear_on_submit=True):
        titulo = st.text_input("Título", max_chars=50, placeholder="Informe o título da tarefa")
        descricao = st.text_area("Descrição", max_chars=250, placeholder="Detalhes ou observações")
        categoria = st.selectbox("Categoria", CATEGORIAS)
        prioridade = st.selectbox("Prioridade", PRIORIDADES)
        data = st.date_input("Data da tarefa", value=datetime.today())
        hora = st.time_input("Hora da tarefa", value=datetime.now().strftime("%H:%M"))
        submit = st.form_submit_button("Adicionar Tarefa")

    if submit:
        if not titulo.strip():
            st.error("O título da tarefa é obrigatório.")
        else:
            hora_str = hora.strftime("%H:%M")
            try:
                adicionar_tarefa(
                    st.session_state.usuario_logado,
                    titulo,
                    descricao,
                    categoria,
                    prioridade,
                    data.strftime("%Y-%m-%d"),
                    hora_str,
                    False,
                )
                st.success("Tarefa adicionada com sucesso!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao adicionar tarefa: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Filtros modernos alinhados horizontalmente e estilizados
    st.subheader("🔎 Filtrar e Ordenar Tarefas")

    col1, col2, col3, col4 = st.columns([1.5,1.5,1.5,1.8])
    filtro_categoria = col1.selectbox("Categoria", ["Todas"] + CATEGORIAS)
    filtro_prioridade = col2.selectbox("Prioridade", ["Todas"] + PRIORIDADES)
    mostrar_concluidas = col3.checkbox("Mostrar concluídas", value=True)
    ordem_data_asc = col4.checkbox("Data crescente", value=True)

    tarefas = carregar_tarefas_do_usuario()

    # Aplicar filtros
    if filtro_categoria != "Todas":
        tarefas = [t for t in tarefas if t["categoria"] == filtro_categoria]
    if filtro_prioridade != "Todas":
        tarefas = [t for t in tarefas if t["prioridade"] == filtro_prioridade]
    if not mostrar_concluidas:
        tarefas = [t for t in tarefas if not t["concluida"]]

    tarefas.sort(key=lambda t: t["data"], reverse=not ordem_data_asc)

    # Exportar CSV com botão estilizado
    tarefa_objs = [Tarefa(t["titulo"], t["descricao"], t["categoria"], t["prioridade"], t["data"], t["hora"], t["concluida"]) for t in tarefas]
    csv_content = exportar_tarefas_csv(tarefa_objs)

    st.download_button(
        label="📥 Exportar Tarefas para CSV",
        data=csv_content,
        file_name="tarefas_exportadas.csv",
        mime="text/csv",
        key="btn_export_csv",
        help="Baixe suas tarefas para backup ou uso externo",
        use_container_width=True,
    )

    # Exibição das tarefas cards estilizados
    st.subheader("📋 Minhas Tarefas")

    if not tarefas:
        st.info("Nenhuma tarefa encontrada para os filtros aplicados.")
        return

    for tarefa in tarefas:
        bg_color = COR_PRIORIDADE.get(tarefa["prioridade"], "rgba(255,255,255,0.8)")
        borda_cor = {
            "Alta": "#ff4d4f",
            "Média": "#ffc107",
            "Baixa": "#28a745",
        }.get(tarefa["prioridade"], "#ddd")

        estilo_titulo = "concluida" if tarefa["concluida"] else ""
        with st.container():
            st.markdown(
                f"""
                <div class="card-tarefa" style="background-color: {bg_color}; border-left-color: {borda_cor};">
                    <div class="titulo-tarefa {estilo_titulo}">
                        {ICONE_PRIORIDADE[tarefa["prioridade"]]} [{tarefa["data"].strftime('%d/%m/%Y')}] {tarefa["titulo"]} {ICONE_CATEGORIA.get(tarefa["categoria"], '')}
                    </div>
                    <div class="detalhes-tarefa"><strong>Descrição:</strong> {tarefa["descricao"] or "Sem descrição"}</div>
                    <div class="detalhes-tarefa"><strong>Categoria:</strong> {tarefa["categoria"]}</div>
                    <div class="detalhes-tarefa"><strong>Prioridade:</strong> {tarefa["prioridade"]}</div>
                    <div class="detalhes-tarefa"><strong>Status:</strong> {"Concluída ✅" if tarefa["concluida"] else "Pendente ⏳"}</div>
                    <div class="detalhes-tarefa"><strong>Hora:</strong> {tarefa["hora"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col1, col2, col3 = st.columns([1, 1, 8])
            with col1:
                if not tarefa["concluida"]:
                    if st.button(
                        f"Concluir", key=f"concluir_{tarefa['id']}", help="Marcar como concluída"
                    ):
                        atualizar_tarefa(
                            tarefa["id"],
                            st.session_state.usuario_logado,
                            tarefa["titulo"],
                            tarefa["descricao"],
                            tarefa["categoria"],
                            tarefa["prioridade"],
                            tarefa["data"].strftime("%Y-%m-%d"),
                            True,
                        )
                        st.rerun()
                else:
                    if st.button(
                        f"Desconcluir",
                        key=f"desconcluir_{tarefa['id']}",
                        help="Marcar como pendente",
                    ):
                        atualizar_tarefa(
                            tarefa["id"],
                            st.session_state.usuario_logado,
                            tarefa["titulo"],
                            tarefa["descricao"],
                            tarefa["categoria"],
                            tarefa["prioridade"],
                            tarefa["data"].strftime("%Y-%m-%d"),
                            False,
                        )
                        st.rerun()
            with col2:
                if st.button(f"Editar", key=f"editar_{tarefa['id']}", help="Editar tarefa"):
                    st.session_state.editar_tarefa_id = tarefa["id"]
                    st.session_state.editar_tarefa_data = tarefa
                    st.rerun()
            with col3:
                if st.button(f"Excluir", key=f"excluir_{tarefa['id']}", help="Excluir tarefa"):
                    deletar_tarefa(tarefa["id"], st.session_state.usuario_logado)
                    st.rerun()

    # Tela de edição da tarefa selecionada com formulário elegante
    if st.session_state.editar_tarefa_id is not None:
        tarefa_edit = st.session_state.editar_tarefa_data
        st.markdown("---")
        st.header(f"✏️ Editando a tarefa: {tarefa_edit['titulo']}")

        with st.form("form_editar_tarefa", clear_on_submit=False):
            titulo_edit = st.text_input("Título", value=tarefa_edit["titulo"], max_chars=50)
            descricao_edit = st.text_area("Descrição", value=tarefa_edit["descricao"], max_chars=250)
            categoria_edit = st.selectbox("Categoria", CATEGORIAS, index=CATEGORIAS.index(tarefa_edit["categoria"]))
            prioridade_edit = st.selectbox("Prioridade", PRIORIDADES, index=PRIORIDADES.index(tarefa_edit["prioridade"]))
            data_edit = st.date_input("Data da tarefa", value=tarefa_edit["data"])
            hora_edit = st.time_input("Hora da tarefa", value=datetime.strptime(tarefa_edit["hora"], "%H:%M").time())
            submit_edit = st.form_submit_button("Salvar Alterações")

        if submit_edit:
            if not titulo_edit.strip():
                st.error("O título da tarefa é obrigatório.")
            else:
                atualizar_tarefa(
                    st.session_state.editar_tarefa_id,
                    st.session_state.usuario_logado,
                    titulo_edit,
                    descricao_edit,
                    categoria_edit,
                    prioridade_edit,
                    data_edit.strftime("%Y-%m-%d"),
                    tarefa_edit["concluida"],
                )
                st.session_state.editar_tarefa_id = None
                st.session_state.editar_tarefa_data = None
                st.success("Tarefa atualizada com sucesso!")
                st.rerun()

def main():
    if st.session_state.usuario_logado is None:
        tela_login_cadastro()
    else:
        tela_gerenciamento_tarefas()

if __name__ == "__main__":
    main()

# Footer discreto
st.markdown(
    '<div class="footer">© 2024 Plataforma de Tarefas para Atletas — Desenvolvido com ❤️</div>',
    unsafe_allow_html=True,
)

def mostrar_exercicios_para_iniciantes():
    st.markdown("<h2 style='color: #4CAF50;'>🏋️‍♂️ Exercícios para Iniciantes</h2>", unsafe_allow_html=True)

    grupo_muscular = st.selectbox("Filtrar por grupo muscular:", ["Todos", "Peito", "Pernas", "Abdômen", "Braços"])

    exercicios = [
        {
            "nome": "Agachamento Livre",
            "descricao": "Trabalha pernas e glúteos. Faça 3 séries de 12 repetições.",
            "imagem": "https://www.hipertrofia.org/blog/wp-content/uploads/2021/06/agachamento-livre.jpg",
            "grupo": "Pernas",
            "video": "https://www.youtube.com/watch?v=aclHkVaku9U"
        },
        {
            "nome": "Flexão de Braço",
            "descricao": "Excelente para peito, tríceps e ombros. Faça 3 séries de 10 repetições.",
            "imagem": "https://www.tuasaude.com/media/article/yx/fz/flexao-de-braco_15959_l.jpg",
            "grupo": "Peito",
            "video": "https://www.youtube.com/watch?v=IODxDxX7oi4"
        },
        {
            "nome": "Prancha",
            "descricao": "Trabalha o core e melhora a postura. Segure por 30 segundos, 3 vezes.",
            "imagem": "https://i0.wp.com/www.dicasdemusculacao.org/wp-content/uploads/2016/11/prancha-isometrica.jpg",
            "grupo": "Abdômen",
            "video": "https://www.youtube.com/watch?v=pSHjTRCQxIw"
        },
        {
            "nome": "Rosca Bíceps com Halteres",
            "descricao": "Isola os bíceps. Faça 3 séries de 15 repetições.",
            "imagem": "https://www.hipertrofia.org/blog/wp-content/uploads/2017/01/rosca-biceps.jpg",
            "grupo": "Braços",
            "video": "https://www.youtube.com/watch?v=av7-8igSXTs"
        }
    ]

    # Filtrar por grupo muscular
    if grupo_muscular != "Todos":
        exercicios = [ex for ex in exercicios if ex["grupo"] == grupo_muscular]

    for exercicio in exercicios:
        with st.container():
            st.markdown(f"### {exercicio['nome']}")
            st.image(exercicio["imagem"], use_container_width=True)
            st.markdown(f"📋 {exercicio['descricao']}")
            st.video(exercicio["video"])
            st.markdown("---")

    # Treino da Semana
    st.markdown("<h3 style='color: #2196F3;'>🔥 Treino da Semana (Full Body)</h3>", unsafe_allow_html=True)
    st.markdown("""
    **Segunda-feira:** Agachamento Livre, Flexão de Braço, Prancha  
    **Quarta-feira:** Agachamento, Rosca Bíceps, Prancha  
    **Sexta-feira:** Agachamento, Flexão, Prancha

    Cada exercício: 3 séries | 10–15 repetições (ou 30s no caso da prancha).
    """)
menu = ["Minhas Tarefas", "Cadastrar Tarefa", "Exercícios para Iniciantes", "Sair"]
escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "Exercícios para Iniciantes":
    mostrar_exercicios_para_iniciantes()
