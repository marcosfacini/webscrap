import time
import json
import logging
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .browser import PlaywrightBrowser
from .parser import parse_process_list, parse_process_detail

logger = logging.getLogger(__name__)

class ScraperRunner:
    def __init__(self, base_url: str, headless=True, delay_between_requests=1.0):
        self.base_url = base_url
        self.browser = PlaywrightBrowser(headless=headless, user_agent="Mozilla/5.0 (compatible; eproc-scraper/0.1)")
        self.delay = delay_between_requests

    def start(self):
        self.browser.start()

    def stop(self):
        self.browser.stop()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _goto(self, page, url):
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("load")

    def search_by_name(self, name: str) -> List[Dict]:
        results = []
        with self.browser.new_page() as page:
            self._goto(page, self.base_url)
            page.wait_for_selector('#txtStrParte', state='visible', timeout=10000)
            page.fill('#txtStrParte', name)
            logger.debug(f"Campo txtStrParte preenchido com: {name}")
            page.click('#sbmNovo')
            logger.debug("Botão de consulta clicado")
            page.wait_for_load_state("load")
            time.sleep(self.delay)
            html = page.content()
            list_links = parse_process_list(html, name)
            
            for link in list_links:
                with self.browser.new_page() as detail_page:
                    self._goto(detail_page, link)
                    detail_html = detail_page.content()
                    detail = parse_process_detail(detail_html)
                    results.append({"link": link, "detalhes": detail})
                time.sleep(self.delay)
            logger.info(f"Encontrados {len(results)} processos para: {name}")
        return results

    def run_for_names(self, names: List[str]) -> Dict[str, List[Dict]]:
        data = {}
        self.start()
        try:
            for name in names:
                try:
                    items = self.search_by_name(name)
                    if not items:
                        data[name] = "Nao foram encontrados dados para este nome"
                    else:
                        data[name] = items
                except Exception as e:
                    logger.exception(f"Falha ao processar {name}: {e}")
                    data[name] = {"error": str(e)}
        finally:
            self.stop()
        return data

    def save_json(self, data, path="resultados.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
