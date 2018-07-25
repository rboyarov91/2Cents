import requests
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup


def get_search_page_results(phrase):
    use_secure = True
    url = "www.amazon.com"
    if use_secure:
        url = "https://{}".format(url)
    else:
        url = "http://{}".format(url)

    full_url = "{}/s/field-keywords={}".format(url, phrase.replace(" ", "+"))
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    r = requests.get(url=full_url, headers=headers)
    html_results_id = "atfResults"
    html = r.content
    soup = BeautifulSoup(html, 'html.parser')
    file = open("response.html", "w")
    file.write(html)
    file.close
    products = []
    for li in soup.findAll('li'):
        try:
            h2 = li.find("h2")
            link = h2.parent.get('href').encode("utf-8")
            if not link.startswith(url):
                link = "{}{}".format(url, link)
            item = h2['data-attribute']
            price =  li.find("span", attrs={"class":"a-offscreen"}).contents[0].encode("utf-8")
            dollars = li.find("span", attrs={"class":"sx-price-whole"}).contents[0].encode("utf-8")
            cents = li.find("sup", attrs={"class":"sx-price-fractional"}).contents[0].encode("utf-8")
            price = "${}.{}".format(dollars, cents)
            product_dict = {
                "name": item,
                "price": price,
                "url": link
            }
            products.append(product_dict)
        except Exception as e:
            pass

    for p in products:
        print p
    # print len(products)


if __name__ == "__main__":
    phrase = "timex watch men"
    get_search_page_results(phrase)
