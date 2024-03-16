import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote
import re


def scraper():
    all_news = []
    for i in range(1, 41):
        print(f'Loop {i} is running...')

        # url = f'https://g1.globo.com/politica/index/feed/pagina-{i}.ghtml'
        url = f'https://g1.globo.com/busca/?q=pol%C3%ADtica&ps=on&order=recent&species=not%C3%ADcias&from=2022-08-31T00%3A00%3A00-0400&to=2022-11-01T23%3A59%3A59-0400&page={i}&ajax=1'

        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

        page = requests.get(url, headers=browsers)
        resposta = page.text
        soup = BeautifulSoup(resposta, 'html.parser')
        # noticias = soup.find_all('a', attrs={'class': 'feed-post-figure-link gui-image-hover'})
        noticias = soup.select('.results__list a')

        for noticia in noticias:
            # title = noticia.find('img').get('title')
            # title = noticia.find('div', class_='widget--info__title product-color').text.strip()
            try:
                title = noticia.find('div', class_='widget--info__title product-color').text.strip()
            except AttributeError:
                print("Falha ao extrair o título. Pulando para próxima notícia.")
                continue
            url = unquote(noticia.get('href'))
            pattern = re.compile(r'https://[^\s&"]+\.ghtml')
            match = pattern.search(url)
            if match:
                # Extract the matched substring
                result = match.group()
                all_news.append({'Title': title, 'URL': result if result else ''})
                print(result)
            else:
                print("No match found.")
            # all_news.append({'Title': title, 'URL': url if url else ''})

    return all_news


if __name__ == '__main__':
    scraping_result = scraper()

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(scraping_result)

    # Ensure 'Title' and 'URL' columns are present in the DataFrame
    df = df[['Title', 'URL']].dropna()

    # Save the DataFrame to a CSV file
    df.to_csv('g1_politica.csv', index_label='RowNames', sep=';')
