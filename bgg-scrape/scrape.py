import requests
from bs4 import BeautifulSoup

urls = ['https://boardgamegeek.com/browse/boardgame']

for i in range(2,5):
    urls.append('https://boardgamegeek.com/browse/boardgame/page/' + str(i))
    

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print("hey")

    rows = soup.find_all('tr', id=lambda x: x and x.startswith('row_'))

    for row in rows:
        rank = row.find('td', class_='collection_rank').get_text(strip=True)
        
        # The game name and link are within the first <a> tag inside the 'collection_objectname' class td
        game_link_tag = row.find('td', class_='collection_objectname').find('a', class_='primary', href=True)
        game_name = game_link_tag.get_text(strip=True)
        game_link = game_link_tag['href']
        
        print(f"{rank},{game_name},{game_link}")