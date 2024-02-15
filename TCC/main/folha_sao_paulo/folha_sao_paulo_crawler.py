import requests
import pandas as pd
from bs4 import BeautifulSoup


def scraper():
    all_news = []
    for i in range(1, 653, 25):
        print(f'Loop {i} is running...')
        url = f'https://search.folha.uol.com.br/search?q=pol%C3%ADtica&site%5B%5D=online%2Fpaineldoleitor&sd=31%2F08%2F2022&ed=01%2F11%2F2022&periodo=personalizado&sr={i}&results_count=653&search_time=1%2C062&url=https%3A%2F%2Fsearch.folha.uol.com.br%2Fsearch%3Fq%3Dpol%25C3%25ADtica%26site%255B%255D%3Donline%252Fpaineldoleitor%26sd%3D31%252F08%252F2022%26ed%3D01%252F11%252F2022%26periodo%3Dpersonalizado%26sr%3D51'

        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

        page = requests.get(url, headers=browsers)
        resposta = page.text
        soup = BeautifulSoup(resposta, 'html.parser')

        result_dict = {}

        links = soup.find_all('div', attrs={'class': 'c-headline__content'})

        for link in links[0:25]:
            href = link.find('a')['href']
            title = link.find('a').find('h2').get_text(strip=True)

            # Save results into the dictionary
            print("Link: " + href)
            print("Titulo: " + title)
            print("\n")
            result_dict[href] = title
            all_news.append({'Title': title, 'URL': href if href else ''})

        # print(result_dict)

    return all_news


if __name__ == '__main__':
    scraping_result = scraper()

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(scraping_result)

    # Ensure 'Title' and 'URL' columns are present in the DataFrame
    df = df[['Title', 'URL']].dropna()

    # Save the DataFrame to a CSV file
    df.to_csv('folha_sao_paulo.csv', index_label='RowNames', sep=';')
