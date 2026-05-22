import requests
from bs4 import BeautifulSoup

url = "https://habr.com/ru/companies/gnivc/news/1037538/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

title = soup.find("h1", class_="post__title").text.strip()

author = soup.find("a", class_="user-info__nickname").text.strip()

date = soup.find("time", class_="datetime")["datetime"]

print(f"Заголовок: {title}")
print(f"Автор: {author}")
print(f"Дата: {date}")
