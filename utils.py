"""
utils.py

Contém funções utilitárias para a aplicação, como exportar tarefas para CSV.
"""

import csv
from io import StringIO
from typing import List
from models import Tarefa
import streamlit as st

def exportar_tarefas_csv(tarefas: List[Tarefa]):
    """
    Gera um CSV em memória das tarefas recebidas e retorna o conteúdo.
    Utilizado para permitir download/exportação das tarefas.
    """
    output = StringIO()
    writer = csv.writer(output)
    # Cabeçalho do CSV
    writer.writerow(['Título', 'Descrição', 'Categoria', 'Prioridade', 'Data', 'Concluída'])

    for tarefa in tarefas:
        writer.writerow([
            tarefa.titulo,
            tarefa.descricao,
            tarefa.categoria,
            tarefa.prioridade,
            tarefa.data.strftime("%d/%m/%Y"),
            "Sim" if tarefa.concluida else "Não"
        ])

    return output.getvalue()

def mostrar_imagem_de_fundo():
    """
    Exibe uma imagem de fundo discreta e neutra para a aplicação, 
    usando um link público mais suave do Pexels.
    """
    imagem_url = "https://images.pexels.com/photos/20974/pexels-photo.jpg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{imagem_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            filter: brightness(0.85) grayscale(0.4);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
