# 📋 Task Manager

Um sistema simples e funcional de gerenciamento de tarefas desenvolvido em **Python**, com foco na organização, clareza de código e boas práticas de desenvolvimento.

---

## 📌 Sobre o Projeto

O **Task Manager** permite que o usuário crie, visualize, atualize e remova tarefas com facilidade. A aplicação foi desenvolvida com fins educacionais, como parte de um projeto para praticar estruturas de dados, modularização de código e manipulação de arquivos ou banco de dados.

Este projeto é ideal para quem deseja compreender os fundamentos do desenvolvimento back-end com Python de forma prática.

---

## 🚀 Funcionalidades

- ✅ **Cadastro de Tarefas:** Criação de tarefas com título, descrição e prioridade
- 📄 **Listagem de Tarefas:** Exibição organizada das tarefas registradas
- ✏️ **Edição de Tarefas:** Atualização de dados de uma tarefa específica
- ❌ **Remoção de Tarefas:** Exclusão definitiva de tarefas
- 💾 **Persistência:** Salvamento dos dados via arquivos locais (`.txt`, `.json`, `.csv`) ou banco de dados (caso aplicável)
- ⏱️ **Data de Criação / Prazo de Conclusão:** Controle opcional de prazos

---

## 🛠️ Tecnologias e Conceitos

- **Linguagem:** Python 3.x
- **Módulos Padrão:** `os`, `datetime`, `json`, `csv` (dependendo da versão final)
- **Estrutura Modular:** Separação em funções e arquivos
- **Persistência:** Arquivos locais ou banco de dados (ex: SQLite)
- **Estilo de Código:** PEP8

---

## 📂 Estrutura do Projeto

task_manager/
├── main.py
├── tarefa.py
├── gestor.py
├── utils.py
├── tarefas.json # ou .csv/.txt, dependendo do formato escolhido
└── README.md

task_manager/
├── main.py            # Arquivo principal de execução
├── tarefa.py          # Classe e lógica das tarefas
├── gestor.py          # Regras de negócio e fluxo
├── utils.py           # Funções auxiliares
├── tarefas.json       # Arquivo de armazenamento
└── README.md
🛠️ Tecnologias Utilizadas
Python 3.10+

Módulos padrão: datetime, json, os

(Opcional) sqlite3, csv, argparse, etc.

Estilo PEP8 com docstrings

▶️ Como Executar Localmente
no powershell
python -m streamlit run app.py
bash
Copiar
Editar
# Clone o repositório
git clone https://github.com/seu-usuario/task_manager.git

# Acesse a pasta
cd task_manager

# Execute o programa
python main.py
📈 Status do Projeto
✅ Concluído – Pronto para uso e testes

