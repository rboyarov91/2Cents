import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import datetime

HEADERS ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
dir_path = os.path.dirname(os.path.realpath(__file__))
cached_search_page_file_name = "cached_search_page.html"
cached_search_page_file_path = os.path.join(dir_path, "cached_pages", cached_search_page_file_name)

class HistoryRecord():
    def __init__(self, value, time):
        self.value = value
        self.time = time

class AmazonProductInfo:

    def __init__(self, link, name, id):
        self.link = str(link)
        self.name = str(name)
        self.id = str(id)

        self.current_num_reviews = None
        self.current_review_ratio = None
        self.num_review_history = []
        self.review_ratio_history = []

        self.price = None
        self.price_history = []

    def set_current_review_stats(self, num_reviews, review_ratio):
        self.current_num_reviews = num_reviews
        self.current_review_ratio = review_ratio
        t = datetime.datetime.now().microsecond
        self.num_review_history.append(HistoryRecord(num_reviews, t))
        self.review_ratio_history.append(HistoryRecord(review_ratio, t))

    def set_current_price(self, price):
        self.price = price
        t = datetime.datetime.now().microsecond
        self.price_history.append(HistoryRecord(price, t))

    def get_most_recent_num_review_update(self):
        return self.num_review_history[-1].time

    def get_most_recent_review_ratio_update(self):
        return self.review_ratio_history[-1].time

    def get_most_recent_price_udpate(self):
        return self.price_history[-1].time

    def __str__(self):
        s = "Item: {}\nLink: {}".format(self.name, self.link)
        if self.price is not None:
            s = "{}\nprice: ${}".format(s, self.price)
        if self.current_num_reviews is not None:
            s = "{}\nCustomer Reviews: {}".format(s, self.current_num_reviews)
        if self.current_review_ratio is not None:
            s = "{}\nReviews: {}/5".format(s, self.current_review_ratio*100/20)
        s = "{}\n".format(s)
        return s

def sort_by_num_reviews(products, descending=True):
    #print [p.current_num_reviews for p in products]
    products.sort(key=lambda x: x.current_num_reviews, reverse=descending)
    return products

def sort_by_review_score(products, descending=True):
    products.sort(key=lambda x: x.current_review_ratio, reverse=descending)
    return products


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
            dollars = li.find("span", attrs={"class":"sx-price-whole"}).contents[0].encode("utf-8")
            cents = li.find("sup", attrs={"class":"sx-price-fractional"}).contents[0].encode("utf-8")
            price = "{}.{}".format(dollars, cents)
            price = float(price)
            split_link = np.array(link.split("/"))
            id = split_link[np.where(split_link == "dp")[0] + 1][0]
            try:

                stars_string = li.find("span", attrs={"name":id}).find("i").find("span").contents[0].encode("utf-8")
                top_value = float(stars_string.split(" ")[0])
                bottom_value = float(stars_string.split(" ")[3])
                ratio_percent = top_value / bottom_value
            except Exception as e:
                #print e
                ratio_percent = None
            try:
                num_reviews_string = li.find("span", attrs={"name":id}).parent.find("a", attrs={"class":"a-size-small"}).contents[0].encode("utf-8")
                num_reviews = int(num_reviews_string.replace(",", ""))
            except Exception as e:
                #print e
                num_reviews = None
            product = AmazonProductInfo(link, item, id)
            #print product
            product.set_current_price(price)
            product.set_current_review_stats(num_reviews, ratio_percent)
            #print product
            products.append(product)
        except Exception as e:
            #print "Not adding"
            #print e
            pass
    return products

def get_product_info(url):
    product = {}
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
    p = AmazonProductInfo("http://www.amazon.com", "Name", "123")
    p.set_current_price(23)
    print p.id
