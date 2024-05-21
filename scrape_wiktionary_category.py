import requests
import os
from bs4 import BeautifulSoup
import time

def get_words_from_page(soup):
    links = soup.find_all('a')
    filters = ['Appendix', 'Categor', 'Help', 'Special', 'Wiktionary']
    words = [x.get_text() for x in links if x.get('href') and '/wiki/' in x.get('href') and all ([y not in x.get('href') for y in filters])]
    return words

def scrape_wiktionary_category(url):
    words = []
    page_number = 1
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        words.extend(get_words_from_page(soup))
        print(f'Scraped page {page_number}.')
        page_number += 1
        next_page_link = soup.find('a', string = 'next page')
        if not next_page_link:
            print('Completed.')
            break 
        url = 'https://en.wiktionary.org' + next_page_link.get('href')
        time.sleep(2)
    if not os.path.exists('Output'):
        os.makedirs('Output')
    with open('Output/words.txt', 'w') as f:
        f.write('\n'.join(sorted(list(set(words)))))

def main():
    url = 'https://en.wiktionary.org/wiki/Category:Galician_terms_with_unknown_etymologies'
    scrape_wiktionary_category(url)

if __name__ == '__main__':
    main()




