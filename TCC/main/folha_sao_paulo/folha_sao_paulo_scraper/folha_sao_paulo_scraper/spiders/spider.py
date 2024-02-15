import scrapy
import pandas as pd
from main.folha_sao_paulo.folha_sao_paulo_scraper.folha_sao_paulo_scraper.items import FolhaSaoPauloScraperItem


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["example.com"]  # Replace with the actual domain

    def __init__(self, *args, **kwargs):
        super(MyspiderSpider, self).__init__(*args, **kwargs)
        self.df = pd.read_csv('~/Repo/TCC/main/folha_sao_paulo/folha_sao_paulo.csv', engine='python', sep=';')
        self.start_urls = self.df.iloc[:, -1].tolist()

    def parse(self, response):
        item = FolhaSaoPauloScraperItem()

        # Extract data from the page
        item['title'] = response.css('title::text').get()
        item['url'] = response.url
        item['content'] = response.css('body::text').get()

        yield item
