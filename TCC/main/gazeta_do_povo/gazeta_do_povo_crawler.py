import requests
import pandas as pd
from bs4 import BeautifulSoup


def scraper():
    all_news = []
    for i in range(2, 12):
        print(f'Loop {i} is running...')
        url = f'https://www.gazetadopovo.com.br/republica/{i}/'
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

        page = requests.get(url, headers=browsers)
        resposta = page.text
        soup = BeautifulSoup(resposta, 'html.parser')

        result_dict = {}

        links = soup.find_all('a', attrs={'class': 'trigger-gtm'})

        for link in links[0:23]:
            href = link.get('href')
            title = link.find('h2', class_='post-title').text.strip()

            # Save results into the dictionary
            print("Link: " + href)
            print("Titulo: " + title)
            print("\n")
            result_dict[href] = title
            all_news.append({'Title': title, 'URL': href if href else ''})

        print(result_dict)

    return all_news


if __name__ == '__main__':
    scraping_result = scraper()

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(scraping_result)

    # Ensure 'Title' and 'URL' columns are present in the DataFrame
    df = df[['Title', 'URL']].dropna()

    # Save the DataFrame to a CSV file
    df.to_csv('gazeta_do_povo.csv', index_label='RowNames', sep=';')
