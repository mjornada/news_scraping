import scrapy
import pandas as pd

# scrapy runspider folha_sao_paulo_scraper/spiders/folha_sao_paulo.py -o output.csv


class FolhaSaoPauloScraperSpider(scrapy.Spider):
    name = 'folha_sao_paulo'

    df = pd.read_csv('/home/az/Repo/TCC/main/folha_sao_paulo/folha_sao_paulo.csv', sep=';')
    links = df['URL'].tolist()
    start_urls = links[:3]

    def parse(self, response):
        print(f"Processing URL: {response.url}")
        teste_elements = response.xpath(
            "//main[@id='conteudo']/article[@id='c-news']/div[@class='block'][2]/div[@class='container j-paywall']"
            "/div[@class='flex flex--gutter flex--col flex--md-row']/div[@class='flex-cell']/div[@class='row']"
            "/div[@class='col col--md-1-1 col--lg-12-18']/div[@class='c-news__content']/div[@class='c-news__body']/p")

        # Extract text from each element individually
        paragraphs = [element.xpath('string()').get().strip() for element in teste_elements]

        # Combine paragraphs into a single string
        context_text_without_tags = ' '.join(paragraphs)

        # Print for debugging
        print(context_text_without_tags)

        yield {
            'corpo': context_text_without_tags
        }
