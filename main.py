import requests
from bs4 import BeautifulSoup
from db import HouseManager, engine

manager = HouseManager(engine=engine)

def get_html(URL):
    response = requests.get(URL)
    return response.text


def get_post_links(html):
    post_links = []
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("div", {"class": "listings-wrapper"})
    posts = table.find_all("div", {"class": "main-wrapper"})
    for post in posts:
        href = post.find("a").get("href")
        post_url = "https://www.house.kg" + href
        post_links.append(post_url)
    return post_links



def write_data(data):
    result = manager.insert_house(data)
    return result


def get_post_details(html):
    soup = BeautifulSoup(html, "html.parser")
    name_table = soup.find("div", {"class": "details-header"}).find("div", {"style": "position: relative;"})
    name = name_table.find("div", {"class": "left"}).find("h1").text.strip()
    price_table = soup.find("div", {"class": "details-header"}).find("div", {"class": "right prices-block"}).find("div", {"class": "sep main"})
    price_usd = price_table.find("div", {"class": "price-dollar"}).text.strip()
    price_kgs = price_table.find("div", {"class": "price-som"}).text.strip()
    mobile_table = soup.find("div", {"class": "phone-fixable-block"}).find("div", {"class": "right"})
    mobile = mobile_table.find("div", {"class": "number"}).text.strip()
    data = {
        "title": name,
        "som": price_kgs,
        "dollar": price_usd,
        "mobile": mobile
    }
    return data




def main():
    site = "https://www.house.kg"
    detail_url = "/kupit-kvartiru?region=1&town=2&district=5,2&child_district=122,133,8,9,10&has_mortgage=1&sort_by=upped_at%20desc&page="
    page = 1
    while page != 8:
        URL = site + detail_url + str(page)
        page += 1
        html = get_html(URL)
        post_urls = get_post_links(html)
        for url in post_urls:
            post_data = get_post_details(get_html(url))
            write_data(data=post_data)


if __name__ == "__main__":
    manager.create_table()
    main()