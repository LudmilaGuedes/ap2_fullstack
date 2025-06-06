import streamlit as st
import requests
import pandas as pd
import time

API_URL = "http://localhost:8000/api/administracao/alunos"
SCRAPING_URL = "http://127.0.0.1:8000/scrape/"
DADOS_URL = "http://127.0.0.1:8000/obter_dados/"  # Nova rota para buscar os dados coletados

st.title("Sistema de Gerenciamento")

# Sidebar para navegação entre as seções
opcao = st.sidebar.selectbox("Menu", [
    "Listar Alunos",
    "Buscar Aluno por ID",
    "Cadastrar Aluno",
    "Atualizar Aluno",
    "Deletar Aluno",
    "Iniciar Web Scraping"
])

if opcao == "Listar Alunos":
    st.header("Lista de Alunos")
    if st.button("Carregar alunos"):
        response = requests.get(API_URL)
        if response.status_code == 200:
            alunos = response.json()
            df_alunos = pd.DataFrame(alunos)
            st.dataframe(df_alunos, height=400, width=1000)  # Ajuste de tamanho
        else:
            st.error("Erro ao buscar alunos. Verifique a API.")

elif opcao == "Iniciar Web Scraping":
    st.header("Iniciar Web Scraping")
    if st.button("Executar Scraping"):
        with st.spinner("Executando scraping... Aguarde!"):
            response = requests.get(SCRAPING_URL)

        if response.status_code == 200:
            st.success("Scraping iniciado com sucesso! Aguardando a coleta de dados...")

            # Aguarda um tempo para garantir que os dados sejam processados no backend
            time.sleep(10)

            # Faz a requisição para obter os dados coletados após o scraping
            response_dados = requests.get(DADOS_URL)
            if response_dados.status_code == 200:
                json_data = response_dados.json()
                st.success("Dados coletados com sucesso!")

                # Exibir os dados coletados
                if "dados" in json_data and json_data["dados"]:
                    df_imoveis = pd.DataFrame(json_data["dados"])
                    st.dataframe(df_imoveis, height=500, width=1000)
                else:
                    st.warning("Nenhum dado foi coletado. Verifique os filtros de busca.")

            else:
                st.error(f"Erro ao buscar os dados coletados: Código {response_dados.status_code}")
        else:
            st.error(f"Erro ao iniciar o scraping: Código {response.status_code}")
