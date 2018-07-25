import requests
from bs4 import BeautifulSoup
import os

HEADERS ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
dir_path = os.path.dirname(os.path.realpath(__file__))
cached_search_page_file_name = "cached_search_page.html"
cached_search_page_file_path = os.path.join(dir_path, "cached_pages", cached_search_page_file_name)


def get_search_page_results(phrase, use_cached=False):
    use_secure = True
    url = "www.amazon.com"
    if use_secure:
        url = "https://{}".format(url)
    else:
        url = "http://{}".format(url)

    full_url = "{}/s/field-keywords={}".format(url, phrase.replace(" ", "+"))
    if use_cached:
        with open(cached_search_page_file_path, 'r') as content_file:
            html = content_file.read()
        soup = BeautifulSoup(html, 'html.parser')
    else:
        r = requests.get(url=full_url, headers=HEADERS)
        html = r.content
        soup = BeautifulSoup(html, 'html.parser')
        file = open(cached_search_page_file_path, "w")
        file.write(html)
        file.close
    products = []
    for li in soup.findAll('li'):
        try:
            h2 = li.find("h2")
            link = h2.parent.get('href').encode("utf-8")
            if not link.startswith(url):
                link = "{}{}".format(url, link)
            item = h2['data-attribute'].encode("utf-8")
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
    return products

def get_product_info(product):
    url = product['url']
    r = requests.get(url=url, headers=HEADERS)
    html = r.content
    # file = open("product.html", "w")
    # file.write(html)
    # file.close
    soup = BeautifulSoup(html, 'html.parser')
    try:
        num_reviews = int(soup.find("span", id="acrCustomerReviewText").contents[0].encode("utf-8").split(" ")[0].replace(',', ''))
        product['num_reviews'] = num_reviews
        ratio_string = soup.find("span", id="acrPopover").find('span', attrs={"class": "a-icon-alt"}).contents[0].encode("utf-8")
        print ratio_string
        top_value = float(ratio_string.split(" ")[0])
        bottom_value = float(ratio_string.split(" ")[3])
        ratio_percent = top_value / bottom_value
        product['ratio'] = ratio_percent
    except Exception as e:
        product['num_reviews'] = None
        product['ratio'] = None
        print "Couldn't find reviews for page with url {}".format(url)
        print e

    return product

def debug():
    with open(cached_search_page_file_path, 'r') as content_file:
        content = content_file.read()
    print content
