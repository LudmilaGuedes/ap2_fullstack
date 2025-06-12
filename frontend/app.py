import streamlit as st
import requests
import pandas as pd
import time

# Definição das URLs da API
BASE_URL = "http://localhost:8000/api/administracao/alunos"
SCRAPING_URL = "http://127.0.0.1:8000/scrape/"
DADOS_URL = "http://127.0.0.1:8000/obter_dados/"

st.title("Sistema de Gerenciamento")

# Sidebar para navegação
opcao = st.sidebar.selectbox("Menu", [
    "Listar Alunos",
    "Buscar Aluno por ID",
    "Cadastrar Aluno",
    "Atualizar Aluno",
    "Deletar Aluno",
    "Iniciar Web Scraping"
])

# Função para exibir DataFrame
def exibir_dataframe(dados, mensagem_sucesso, mensagem_erro):
    """Exibe um DataFrame com mensagens de sucesso/erro."""
    if dados:
        df = pd.DataFrame(dados)
        st.success(mensagem_sucesso)
        st.dataframe(df, height=500, width=1000)
    else:
        st.warning(mensagem_erro)

# Listar Alunos
if opcao == "Listar Alunos":
    st.header("Lista de Alunos")
    if st.button("Carregar alunos"):
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            alunos = response.json()

            for aluno in alunos:
                aluno["cep"] = aluno["cep"]["cep"] if aluno["cep"] else None  # Extrai o valor correto
                aluno["carro"] = aluno["carro"]["especificacao"] if aluno["carro"] else None  # Extrai o nome do carro

            df_alunos = pd.DataFrame(alunos)
            st.success("Alunos carregados com sucesso!")
            st.dataframe(df_alunos, height=500, width=1000)
        else:
            st.error("Erro ao buscar alunos. Verifique a API.")



# Buscar Aluno por ID
elif opcao == "Buscar Aluno por ID":
    st.header("Buscar Aluno por ID")
    aluno_id = st.number_input("ID do aluno", min_value=1, step=1)

    if st.button("Buscar"):
        response = requests.get(f"{BASE_URL}/{aluno_id}")
        
        if response.status_code == 200:
            aluno = response.json()

            # Converte para DataFrame com apenas uma linha
            df_aluno = pd.DataFrame([aluno])

            st.success("Aluno encontrado!")
            st.table(df_aluno)  # Exibe como tabela, garantindo apenas uma linha
        else:
            st.error("Aluno não encontrado.")


# Cadastrar Aluno
elif opcao == "Cadastrar Aluno":
    st.header("Cadastrar Aluno")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        cep = st.text_input("CEP")
        carro = st.number_input("ID do Carro", min_value=0, step=1)
        if st.form_submit_button("Cadastrar"):
            data = {
                "nome_aluno": nome,
                "email": email,
                "cep": cep or None,
                "carro": carro if carro != 0 else None
            }
            response = requests.post(BASE_URL, json=data)
            if response.status_code in [200, 204]:
                st.success("Aluno cadastrado com sucesso!")


# Atualizar Aluno
elif opcao == "Atualizar Aluno":
    st.header("Atualizar Aluno")
    with st.form("form_atualizar"):
        id_aluno = st.number_input("ID", min_value=1, step=1)
        novo_nome = st.text_input("Novo nome")
        novo_email = st.text_input("Novo email")
        novo_cep = st.text_input("Novo CEP")
        novo_carro = st.number_input("Novo ID do Carro", min_value=0, step=1)
        if st.form_submit_button("Atualizar"):
            data = {
                "nome_aluno": novo_nome,
                "email": novo_email,
                "cep": novo_cep or None,
                "carro": novo_carro if novo_carro != 0 else None
            }
            response = requests.put(f"{BASE_URL}/{id_aluno}", json=data)
            if response.status_code in [200, 204]:
                st.success("Aluno atualizado com sucesso!")
            else:
                st.error(f"Erro ao atualizar aluno: Código {response.status_code}")

# Deletar Aluno
elif opcao == "Deletar Aluno":
    st.header("Deletar Aluno")
    id_delete = st.number_input("ID do aluno", min_value=1, step=1, key="delete")
    
    if st.button("Deletar"):
        response = requests.delete(f"{BASE_URL}/{id_delete}")

        if response.status_code in [200, 204]:  # Aceita ambos os códigos como sucesso
            st.success("Aluno deletado com sucesso!")
        elif response.status_code == 404:
            st.warning("Esse aluno já foi excluído ou não existe.")
        else:
            st.error(f"Erro ao deletar aluno: Código {response.status_code}")

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

            else:
                st.error(f"Erro ao buscar os dados coletados: Código {response_dados.status_code}")
        else:
            st.error(f"Erro ao iniciar o scraping: Código {response.status_code}")