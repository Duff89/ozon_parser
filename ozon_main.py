import time
from playwright.sync_api import sync_playwright


class OzonSellerParse:
    def __init__(self, keyword: str):
        self.keyword = keyword

    def __page_down(self, page):
        page.evaluate('''
                                const scrollStep = 200; // Размер шага прокрутки (в пикселях)
                                const scrollInterval = 100; // Интервал между шагами (в миллисекундах)

                                const scrollHeight = document.documentElement.scrollHeight;
                                let currentPosition = 0;
                                const interval = setInterval(() => {
                                    window.scrollBy(0, scrollStep);
                                    currentPosition += scrollStep;

                                    if (currentPosition >= scrollHeight) {
                                        clearInterval(interval);
                                    }
                                }, scrollInterval);
                            ''')

    def __get_seller_name(self, url: str):
        self.page2 = self.context.new_page()
        self.page2.goto(url=url)

        self.__page_down(self.page2)
        try:
            self.page2.wait_for_selector(f':text("Продавец")')
            elements = self.page2.query_selector_all('a[href^="https://www.ozon.ru/sell"]')
            seller_name = elements[1].inner_text()
            print(seller_name)
        except Exception:
            return

    def __get_links(self):
        self.page.wait_for_selector("#paginatorContent")
        self.__page_down(self.page)
        self.page.wait_for_selector(f':text("Дальше")')

        search_result = self.page.query_selector("#paginatorContent")
        links = search_result.query_selector_all(".tile-hover-target")
        print(len(links))
        for count, link in enumerate(links):
            if count > 5: break
            url = "https://ozon.by" + link.get_attribute('href')
            self.__get_seller_name(url=url)

    def parse(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto("https://ozon.by/")
            self.page.get_by_placeholder("Искать на Ozon").type(text=self.keyword, delay=0.3)
            self.page.query_selector("button[type='submit']").click()
            self.__get_links()


if __name__ == "__main__":
    OzonSellerParse("вентилятор").parse()
    time.sleep(20)
