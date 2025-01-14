import scrapy
import pandas as pd


#  ~/repo/news_scraping/TCC/main/cnn_brasil
# scrapy runspider cnn_brasil_scraper/cnn_brasil_scraper/spiders/cnn_brasil.py -o output.csv --set delimiter=";"
# /home/az/repo/news_scraping/TCC/main/g1_politica/spyder/spyder/spiders/g1_politica.py

class CnnBrasilScraperSpider(scrapy.Spider):
    delimiter = ";"
    name = 'cnn_brasil'

    df = pd.read_csv('/home/az/repo/news_scraping/TCC/main/cnn_brasil/cnn_politica.csv', sep=';')
    # print(df['URL'])
    links = df['URL'].tolist()
    # print(links[0:1])
    # start_urls = links[:1]
    start_urls = links
    data_list = []

    def parse(self, response):
        print(f"Processing URL: {response.url}")

        teste_elements = response.xpath("//div[@class='site__content']/div[@class='container']/div[@class='row']/main[@class='posts col__list']/article")

        print("\n")
        print("################################################################################################")
        print("teste_elements: \n", teste_elements)
        print("\n")
        print("################################################################################################")

        # Extract text from each element individually
        paragraphs = [element.xpath('string()').get().strip() for element in teste_elements]
        print("\n")
        print("################################################################################################")
        print("paragraphs: \n", paragraphs)
        print("\n")
        print("################################################################################################")

        # Combine paragraphs into a single string
        context_text_without_tags = ' '.join(paragraphs)

        # Print for debugging
        print("\n")
        print("################################################################################################")
        print("context_text_without_tags: \n", context_text_without_tags)
        print("\n")
        print("################################################################################################")

        if context_text_without_tags == '':
            print(f'Eu sou string vazia.')

            elementos_B = response.xpath("//main[@id='conteudo']/article[@id='c-news']/div[@class='block'][2]/div[@class='container j-paywall']"
                                         "/div[@class='flex flex--gutter flex--col flex--md-row']/div[@class='flex-cell']/div[@class='row']"
                                         "/div[@class='col col--md-1-1 col--lg-12-18']/div[@class='c-news__content']/div[@class='c-news__body']/div")
            print("\n")
            print("################################################################################################")
            print("elementos_B: \n", elementos_B)
            print("\n")
            print("################################################################################################")

            # Extract text from each element individually
            paragraphs = [element.xpath('string()').get().strip() for element in elementos_B]
            print("\n")
            print("################################################################################################")
            print("paragraphs: \n", paragraphs)
            print("\n")
            print("################################################################################################")

            # Combine paragraphs into a single string
            context_text_without_tags = ' '.join(paragraphs)

            # Print for debugging
            print("\n")
            print("################################################################################################")
            print("context_text_without_tags: \n", context_text_without_tags)
            print("\n")
            print("################################################################################################")

        self.data_list.append({'start_url': response.url, 'corpo': context_text_without_tags})

        yield {
            'start_url': response.url,
            # 'corpo': context_text_without_tags
            'corpo': "teste"
        }

    def closed(self, reason):
        # Convert the list to a DataFrame and save to CSV
        df_output = pd.DataFrame(self.data_list)
        df_output.to_csv('output_scrapy.csv', sep=';', index=False)
