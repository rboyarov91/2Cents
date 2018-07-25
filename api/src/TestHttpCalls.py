import AmazonSearchUtils

if __name__ == "__main__":
    phrase = "timex watch men"
    products = AmazonSearchUtils.get_search_page_results(phrase, use_cached=True)
    print products
    # updated_products = []
    # for product in products:
    #     updated_products.append(get_product_info(product))
    #
    # for p in updated_products:
    #     print p
