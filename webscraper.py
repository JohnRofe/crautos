from playwright.sync_api import sync_playwright

class WebScraper:

    def __init__(self, url):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        self.page.route('**/*.{png,jpg,jpeg}', lambda route, _: route.abort())
        self.url = url

    def get_html(self, selector = None):
        self.page.goto(self.url)
        if selector:
            self.page.wait_for_selector(selector)
        html = self.page.inner_html('body')
        return html

    def close(self):
        self.browser.close()
        self.playwright.stop()

    


