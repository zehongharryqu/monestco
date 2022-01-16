from scrapy import Spider, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy_playwright.page import PageCoroutine
from scrapy.utils.response import open_in_browser


Detail_Page_Rendering_Required = True

class MonestSpider(CrawlSpider):
    name = 'MonestSpider'
    start_urls = ['https://www.adidas.ca/en/clothing',]

    detail_callback: str = 'sync_parse_detail_page'
    if Detail_Page_Rendering_Required:
        detail_callback = 'async_parse_detail_page'


    rules = (
        # following list pages of clothings
        Rule(LinkExtractor(allow=('clothing\?grid=true&start'))),
        # Extract Item detail pages
        Rule(LinkExtractor(restrict_css='a[data-auto-id=glass-hockeycard-link]', ),
             callback=detail_callback,
             process_request='process_detail_request')
    )

    def sync_parse_detail_page(self, response):
        yield {
            'name': response.css('div[class*=sidebar-wrapper] h1[data-auto-id=product-title] span::text').get(),
            'price': response.css('div[class*=sidebar-wrapper] div[class*=product-price] div['
                                  'class*=gl-price-item]::text').get(),
            'category': response.css('div[data-auto-id=product-category] span::text').get(),
            'description': response.css('div#navigation-target-description p::text').get(),
            'url':  response.url,
            'photo': response.css('section[data-auto-id=image-viewer] img::attr(src)').extract_first(),
        }

    async def async_parse_detail_page(self, response):
        # open_in_browser(response)
        yield {
            'title': response.css('div[class*=sidebar-wrapper] h1[data-auto-id=product-title] span::text').get(),
            'subtitle': response.css('div[data-auto-id=product-category] span::text').get(),
            'price': response.css('div[class*=sidebar-wrapper] div[class*=product-price] div['
                                  'class*=gl-price-item]::text').get(),
            'color': response.css('div[data-auto-id=color-chooser] h5::text').getall()[1],
            'description': response.css('div#navigation-target-description p::text').get(),
            'url': response.url,
            'photo': response.css('section[data-auto-id=image-viewer] img::attr(src)').extract_first(),
        }

    def process_detail_request(self, request, response):
        #enble playwright rendering
        if Detail_Page_Rendering_Required:
            current_meta = request.meta
            current_meta |= dict(
                playwright=True,
                playwright_page_coroutines=[
                    PageCoroutine('wait_for_selector', 'div#navigation-target-description p'),
                ]
            )

        return request



if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            "DOWNLOAD_HANDLERS": {
                "https": "crawler.crawler.ScrapyPlaywrightDownloadHandlerEnhanced.ScrapyPlaywrightDownloadHandlerEnhanced",
                # "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 60000,
        }
    )
    process.crawl(MonestSpider)
    process.start()
