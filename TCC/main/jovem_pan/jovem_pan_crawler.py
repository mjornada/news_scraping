import requests
import pandas as pd
from bs4 import BeautifulSoup


def scraper():
    all_news = []
    # 368 a 300
    for i in range(370, 300, -1):
        print(f'Loop {i} is running...')
        url = f"https://jovempan.com.br/noticias/politica/page/{i}"
        # 17 links por página
        browsers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

        try:
            page = requests.get(url, headers=browsers)
            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            result_dict = {}

            links = soup.find_all('article')

            for link in links[0:18]:
                href = link.find('a')['href']
                title = link.find('span', class_='date').text.strip()
                date = link.find('h2', class_='post-title').text.strip()

                # Save results into the dictionary
                print("Link: " + href)
                print("Titulo: " + title)
                print("Data: " + date)
                print("\n")
                result_dict[href] = title
                all_news.append({'Title': title, 'URL': href if href else '', 'Date': date})
        except:
            print(f"Failed to process page {i}. Skipping to next iteration.")

    return all_news


if __name__ == '__main__':
    scraping_result = scraper()

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(scraping_result)

    # Ensure 'Title' and 'URL' columns are present in the DataFrame
    # df = df[['Title', 'URL']].dropna()

    # Save the DataFrame to a CSV file
    df.to_csv('jovem_pan_politica.csv', index_label='RowNames', sep=';')
