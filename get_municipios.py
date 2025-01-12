import requests
from bs4 import BeautifulSoup

url = 'https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_de_S%C3%A3o_Paulo'

response = requests.get(url)
response.encoding = response.apparent_encoding

soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find_all('tr')

municipios = [row.find('a', title=True).text for row in rows if row.find('a', title=True)]

# Write the file with the correct encoding
with open("municipios.txt", "w", encoding="utf-8") as file:
    for item in municipios:
        file.write(f"{item}\n")