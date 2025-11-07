"""
esse modulo vai ser responsavel por descobrir automaticamente links de atas nos sites dos municipios,
sem depender de caminhos fixos. ele vai usar selenium pra lidar com pags dinamicas (tipo ASP.NET)
e beautifulsoup pra analisar o HTML e encontrar keywords relevantes
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import time
import re

# configs do selenium pra nao abrir janela (modo headless)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--log-level=3")  # esconde logs desnecessarios

def init_driver():
    # inicializa o chrome com selenium manager automaticamente
    from selenium.webdriver.chrome.service import Service
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

# lista de palavras que devem ser ignoradas (pra evitar confundir com politica de investimentos)
BLACKLIST = ["política de investimentos", "politica de investimentos", "policy"]

def is_blacklisted(text: str) -> bool:
    # retorna True se o texto tiver termos da blacklist
    s = (text or "").lower()
    return any(b in s for b in BLACKLIST)

def find_meeting_links(base_url: str, wait_time=3):
    # descobre links relevantes de atas, comites e conselhos sem depender de caminhos fixos
    driver = init_driver()
    driver.get(base_url)
    time.sleep(wait_time)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "lxml")
    links = []

    # keywords que ajudam a identificar links de atas
    keywords = [
        "ata", "reunião", "comitê", "comite", "investimento",
        "conselho", "transparência", "publicações", "documentos"
    ]

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = a.get_text().lower()

        # ignora links irrelevantes (tipo politicas)
        if is_blacklisted(href) or is_blacklisted(text):
            continue

        # verifica se tem keywords relevantes
        if any(k in href.lower() for k in keywords) or any(k in text for k in keywords):
            if not href.startswith("http"):
                href = urljoin(base_url, href)
            if href not in links:
                links.append(href)

    return links