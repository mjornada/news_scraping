import scrapy
import pandas as pd
from scrapy.spiders import CSVFeedSpider
from scrapy.exporters import CsvItemExporter


# scrapy runspider folha_sao_paulo_scraper/spiders/folha_sao_paulo.py -o output.csv --set delimiter=";"


class FolhaSaoPauloScraperSpider(scrapy.Spider):
    delimiter = ";"
    name = 'folha_sao_paulo'

    df = pd.read_csv('/home/az/repo/TCC/main/folha_sao_paulo/folha_sao_paulo.csv', sep=';')
    links = df['URL'].tolist()
    start_urls = links[:653]
    data_list = []

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

        if context_text_without_tags is '':
            print(f'Eu sou string vazia.')

            elementos_B = response.xpath("//main[@id='conteudo']/article[@id='c-news']/div[@class='block'][2]/div[@class='container j-paywall']"
                                         "/div[@class='flex flex--gutter flex--col flex--md-row']/div[@class='flex-cell']/div[@class='row']"
                                         "/div[@class='col col--md-1-1 col--lg-12-18']/div[@class='c-news__content']/div[@class='c-news__body']/div")

            # Extract text from each element individually
            paragraphs = [element.xpath('string()').get().strip() for element in elementos_B]

            # Combine paragraphs into a single string
            context_text_without_tags = ' '.join(paragraphs)

            # Print for debugging
            print(context_text_without_tags)

        self.data_list.append({'start_url': response.url, 'corpo': context_text_without_tags})

        yield {
            'start_url': response.url,
            'corpo': context_text_without_tags
        }

    def closed(self, reason):
        # Convert the list to a DataFrame and save to CSV
        df_output = pd.DataFrame(self.data_list)
        df_output.to_csv('output_pandas.csv', sep=';', index=False)