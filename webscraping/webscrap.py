from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


CAMINHO_RAIZ = Path(__file__).parent
CHROMEDRIVER = CAMINHO_RAIZ / 'drivers' / 'chromedriver'


# cria o navegador com as configuracoes
def create_browser() -> webdriver.Chrome:
    chrome_service = Service(executable_path=str(CHROMEDRIVER))
    chrome_options = webdriver.ChromeOptions()
    # funcao que executa o google em segundo plano, as vezes nao funciona
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu-flag')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_browser = webdriver.Chrome(
        service=chrome_service,
        options=chrome_options
    )

    return chrome_browser


# decorator que sobe um erro caso o link não seja valido
def _verify_link(func):
    def inner(*args, **kwargs):
        try:
            f = func(*args, **kwargs)
            return f
        except:
            raise Exception(
                'Produto não encontrado - Veja se o link está correto')
    return inner


# funcao que pega o preco
@_verify_link
def pick_price(soup: BeautifulSoup):
    find_price = '#price'
    if soup.select_one(find_price):
        select_price = soup.select_one(find_price)
        price = select_price.text
        return price
    find_price2 = 'div#corePriceDisplay_desktop_feature_div > \
                                div > span span.a-offscreen'
    if soup.select(find_price2):
        select_price = soup.select_one(find_price2)
        price = select_price.text
        return price
    find_price3 = '#kindle-price'
    if soup.select(find_price3):
        select_price = soup.select_one(find_price3)
        price = select_price.text
        return price + 'no kindle'


# funcao que pega o nome do produto
@_verify_link
def pick_product_title(soup: BeautifulSoup):
    find_name = '#productTitle'
    select_name = soup.select_one(find_name)
    name = select_name.text
    return name
