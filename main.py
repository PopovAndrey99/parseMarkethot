import requests
from bs4 import BeautifulSoup
import pandas as pd


url_pages = [
    "https://markethot.ru/catalog/avto/?sort=CATALOG_AVAILABLE&order=desc"
    # "https://markethot.ru/catalog/?q=алмазная%20мозаика&s=Найти&PAGEN_2=2",
    # "https://markethot.ru/catalog/?q=алмазная%20мозаика&s=Найти&PAGEN_2=3",
    # "https://markethot.ru/catalog/?q=алмазная%20мозаика&s=Найти&PAGEN_2=4",
    # "https://markethot.ru/catalog/?q=алмазная%20мозаика&s=Найти&PAGEN_2=5"
]


cards = []
for page in url_pages:
    response = requests.get(page)
    soup = BeautifulSoup(response.text, "html.parser")
    headers = soup.find_all(
        "a",
        class_="dark_link switcher-title js-popup-title js-replace-link color-theme-target"
    )

    for header in headers:
        href = "https://markethot.ru" + header.get("href")
        cards.append(href)

print("Ссылки на товары загружены.")
print()

index = 1
data = []
for card in cards:
    response = requests.get(card)
    soup = BeautifulSoup(response.text, "html.parser")
    status = soup.find("div", class_="detail-block ordered-block sku")
    title = soup.find("h1", class_="font_32 switcher-title js-popup-title font_20--to-600")
    title_text = title.get_text(strip=True)

    str_photoes = ""
    photoes = soup.find_all("a", class_="detail-gallery-big__link popup_link fancy fancy-thumbs")
    for photo in photoes:
        href = "https://markethot.ru" + photo.get("href")
        str_photoes += href + ";"

    art = ""
    pr = ""

    if status == None:
        stat = soup.find("span", class_="js-replace-status")
        stat_text = stat.get_text(strip=True)
        if stat_text == "Есть в наличии":
            article = soup.find("span", class_="js-replace-article")
            art = article.get_text(strip=True)
            
            price = soup.find("span", class_="price__new-val font_24")
            pr = price.get_text(strip=True)

            data.append([
                art,
                "",
                str_photoes,
                pr,
                title_text
            ])

            print(str(index) + ". " + art)
            print(title_text)
            print(str_photoes)
            print(pr)
            print()
            index += 1
    else:
        stats = status.find_all("div", class_="catalog-table__info-inner catalog-table__item-wrapper")
        for st in stats:
            available = st.find("div", class_="catalog-table__info-tech")
            avail = available.get_text(strip=True)
            if (avail == "Есть в наличии"):
                inf = st.find("div",class_="catalog-table__info-title linecamp-4 height-auto-t600 font_weight--500 color_222 font_large",)
                text = inf.get_text(strip=True)

                price = status.find("span", class_="price__new-val font_18 font_14--to-600")
                pr = price.get_text(strip=True)

                data.append([
                    art,
                    text,
                    str_photoes,
                    pr,
                    title_text
                ])

                print(str(index) + ". " + art)
                print(title_text)
                print(str_photoes)
                print(pr)
                print()
                index += 1

print()
print("Загрузка товаров завершена.")

df = pd.DataFrame(data)

df.to_excel('данные.xlsx', index=False)
