from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def parse_process_list(html: str, name: str) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    links = []
    table = None
    for tbl in soup.find_all("table"):
        ths = tbl.find_all("th", class_="infraTh")
        for th in ths:
            if th.get_text(strip=True) == "Nome da Parte":
                table = tbl
                break
        if table:
            break
    if not table:
        logger.debug("Tabela com header 'Nome da Parte' não encontrada")
        return links

    for row in table.find_all("tr", class_=["infraTrClara", "infraTrEscura"]):
        td = row.find("td")
        if not td:
            continue
        a_tag = td.find("a")
        if a_tag and a_tag.get_text(strip=True) == name and a_tag.has_attr("href"):
            full_link = f"https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/{a_tag["href"]}"
            links.append(full_link)
    return links

def parse_process_detail(html: str) -> Dict:
    soup = BeautifulSoup(html, "lxml")
    detail = {}
    table = soup.find("table", class_="infraTable")
    if not table:
        logger.debug("Tabela de processos não encontrada")
        return detail

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    try:
        idx_numero = headers.index("Nº Processo")
        idx_autor = headers.index("Autor")
        idx_reu = headers.index("Réu")
    except ValueError:
        logger.debug("Cabeçalhos esperados não encontrados na tabela")
        return detail

    row = table.find("tr", class_="infraTrClara")
    if not row:
        logger.debug("Linha de dados não encontrada na tabela de processos")
        return detail
    cols = row.find_all("td")
    if len(cols) < max(idx_numero, idx_autor, idx_reu) + 1:
        logger.debug("Colunas insuficientes na linha de dados")
        return detail

    numero_processo = cols[idx_numero].get_text(strip=True)
    autor = cols[idx_autor].get_text(strip=True)
    reu = cols[idx_reu].get_text(strip=True)

    detail = {
        "numero_processo": numero_processo,
        "autor": autor,
        "reu": reu
    }
    return detail
