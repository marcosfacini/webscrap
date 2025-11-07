from playwright.sync_api import sync_playwright
import time
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class PlaywrightBrowser:
    def __init__(self, headless=True, user_agent=None, timeout=30000):
        self.headless = headless
        self.user_agent = user_agent
        self.timeout = timeout
        self._pw = None
        self._browser = None

    def start(self):
        logger.debug("Iniciando Playwright browser")
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=self.headless)
        return self

    def stop(self):
        logger.debug("Fechando Playwright browser")
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()

    @contextmanager
    def new_page(self):
        page = self._browser.new_page()
        if self.user_agent:
            page.set_extra_http_headers({"User-Agent": self.user_agent})
        page.set_default_timeout(self.timeout)
        try:
            yield page
        finally:
            page.close()
