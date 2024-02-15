import requests
import pandas as pd
from bs4 import BeautifulSoup


def scraper():
    all_news = []
    for i in range(1, 20):
        print(f'Loop {i} is running...')
        # https: // g1.globo.com / busca /?q = pol % C3 % ADtica & ps = on & order = recent & species = not %C3 % ADcias &
        # from=2022 - 0
        # 8 - 31
        # T00 % 3
        # A00 % 3
        # A00 - 0400 & to = 2022 - 11 - 01
        # T23 % 3
        # A59 % 3
        # A59 - 0400 & page = 40 & ajax = 1
        # page 40 = ultima pagina
        url = f'https://g1.globo.com/politica/index/feed/pagina-{i}.ghtml'
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

        page = requests.get(url, headers=browsers)
        resposta = page.text
        soup = BeautifulSoup(resposta, 'html.parser')
        noticias = soup.find_all('a', attrs={'class': 'feed-post-figure-link gui-image-hover'})

        for noticia in noticias:
            title = noticia.find('img').get('title')
            url = noticia.get('href')
            all_news.append({'Title': title, 'URL': url if url else ''})

    return all_news


if __name__ == '__main__':
    scraping_result = scraper()

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(scraping_result)

    # Ensure 'Title' and 'URL' columns are present in the DataFrame
    df = df[['Title', 'URL']].dropna()

    # Save the DataFrame to a CSV file
    df.to_csv('output_file.csv', index_label='RowNames', sep=';')
