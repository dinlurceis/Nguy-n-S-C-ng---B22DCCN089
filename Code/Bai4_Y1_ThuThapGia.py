from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

data = pd.read_csv('results.csv')
data2 = pd.DataFrame(data)
data_list_has_index_column = data2.values.tolist()
data_list = [row[1:] for row in data_list_has_index_column]
data_dict = {x[0]: x[1:] for x in data_list}

urls = [
    'https://www.footballtransfers.com/us/players/uk-premier-league',
    'https://www.footballtransfers.com/us/players/uk-premier-league/2',
    'https://www.footballtransfers.com/us/players/uk-premier-league/3',
    'https://www.footballtransfers.com/us/players/uk-premier-league/4',
    'https://www.footballtransfers.com/us/players/uk-premier-league/5',
    'https://www.footballtransfers.com/us/players/uk-premier-league/6',
    'https://www.footballtransfers.com/us/players/uk-premier-league/7',
    'https://www.footballtransfers.com/us/players/uk-premier-league/8',
    'https://www.footballtransfers.com/us/players/uk-premier-league/9',
    'https://www.footballtransfers.com/us/players/uk-premier-league/10',
    'https://www.footballtransfers.com/us/players/uk-premier-league/11',
    'https://www.footballtransfers.com/us/players/uk-premier-league/12',
    'https://www.footballtransfers.com/us/players/uk-premier-league/13',
    'https://www.footballtransfers.com/us/players/uk-premier-league/14',
    'https://www.footballtransfers.com/us/players/uk-premier-league/15',
    'https://www.footballtransfers.com/us/players/uk-premier-league/16',
    'https://www.footballtransfers.com/us/players/uk-premier-league/17',
    'https://www.footballtransfers.com/us/players/uk-premier-league/18',
    'https://www.footballtransfers.com/us/players/uk-premier-league/19',
    'https://www.footballtransfers.com/us/players/uk-premier-league/20',
    'https://www.footballtransfers.com/us/players/uk-premier-league/21',
    'https://www.footballtransfers.com/us/players/uk-premier-league/22',
    'https://www.footballtransfers.com/us/players/uk-premier-league/23',
    'https://www.footballtransfers.com/us/players/uk-premier-league/24'
]

player_values = []
for url in urls:
    # khởi động trình duyệt
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # truy cập trang web
    driver.get(url)

    # chờ một chút để trang tải hoàn toàn
    time.sleep(5)

    table = driver.find_element(By.TAG_NAME, 'tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr')

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        for i in range(len(cells)):
            if i % 7 == 1:
                player_name = cells[i].text.split('\n')[0]
                price = cells[i + 3].text
                if player_name in data_dict.keys():
                    player_values.append([player_name, price])

    # đóng trình duyệt
    driver.quit()

df = pd.DataFrame(player_values, columns=[
    'Player',
    'Giá chuyển nhượng'
])
print('Giá chuyển nhượng của từng cầu thủ:')
print(df)
df.to_csv('resultsGiaChuyenNhuong.csv')
