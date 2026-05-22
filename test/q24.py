import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com/")
soup = BeautifulSoup(response.text, "html.parser")

quote = soup.find("span", class_="text").text
author = soup.find("small", class_="author").text

print(f'Цитата: "{quote}", Автор: {author}')
