from selenium import webdriver


def main():
    use_secure = True
    url = "www.amazon.com"
    if use_secure:
        url = "https://{}".format(url)
    else:
        url = "http://{}".format(url)

    phrase = "timex watch men"

    full_url = "{}/s/field-keywords={}".format(url, phrase.replace(" ", "+"))
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    driver = webdriver.PhantomJS()
    driver.get(url)
    print driver



if __name__ == "__main__":
    main()