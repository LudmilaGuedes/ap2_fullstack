# webScraping/scraper.py
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from django.db import connections
from webScraping.models import TbImoveis

def coletar_dados():
    """Função síncrona para capturar e salvar dados via Web Scraping."""

    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")  # Ignora erros SSL
    options.add_argument("--disable-blink-features=AutomationControlled")  # Oculta Selenium
    
    # Inicializa o navegador
    driver = webdriver.Chrome(options=options)

    # Limpa todos os cookies antes de acessar o site
    driver.delete_all_cookies()

    # Acessa o site
    url = 'https://www.dfimoveis.com.br/'
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Parâmetros de pesquisa
    tipo = "VENDA"
    tipos = "CASA"
    estado = "DF"
    cidade = "GUARA"
    quartos = "2"

    # Função para preencher filtros
    def preencher_filtro(by, value, texto):
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        search_field = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "select2-search__field")))
        search_field.send_keys(texto)
        search_field.send_keys(Keys.ENTER)

    preencher_filtro(By.ID, 'select2-negocios-container', tipo)
    preencher_filtro(By.ID, 'select2-tipos-container', tipos)
    preencher_filtro(By.ID, 'select2-estados-container', estado)
    preencher_filtro(By.ID, 'select2-cidades-container', cidade)

    # Seleção de quartos
    element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-quartos-container')))
    element.click()
    sleep(2)  # Aguarde opções carregarem

    opcoesQuartos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'select2-results__option')))
    for opcao in opcoesQuartos:
        if opcao.text.strip() == quartos:
            opcao.click()
            break

    # Busca imóveis
    busca = wait.until(EC.element_to_be_clickable((By.ID, "botaoDeBusca")))
    busca.click()

    lst_imoveis = []
    while True:
        resultado = wait.until(EC.presence_of_element_located((By.ID, "resultadoDaBuscaDeImoveis")))
        elementos = resultado.find_elements(By.TAG_NAME, 'a')

        for elem in elementos:
            imovel = {
                'titulo': elem.find_element(By.CLASS_NAME, 'new-title').text,
                'preco': elem.find_element(By.CLASS_NAME, 'new-price').text,
                'metragem': elem.find_element(By.CLASS_NAME, 'm-area').text,
                'quarto': int(quartos),
                'descricao': elem.find_element(By.CLASS_NAME, 'new-text').text
            }
            lst_imoveis.append(imovel)

        # Verifica se há próximo botão
        botao_proximo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.next')))
        if botao_proximo.get_attribute("class") == "btn disabled next":
            break

        driver.execute_script("arguments[0].click();", botao_proximo)
        sleep(2)  # Espera síncrona

    driver.quit()

    # Limpeza dos dados
    df = pd.DataFrame(lst_imoveis)
    df["preco"] = df["preco"].apply(lambda x: x.split("\n")[0].replace("R$", "").replace(".", "").strip())
    df["metragem"] = df["metragem"].apply(lambda x: x.replace("m²", "").strip())

    # Salvar no banco via Django ORM
    for item in df.to_dict(orient="records"):
        TbImoveis.objects.using("config_scraping").create(**item)

    print("Dados coletados e inseridos no banco!")

    return df.to_dict(orient="records")
