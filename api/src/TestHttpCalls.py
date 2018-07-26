import AmazonSearchUtils
import inspect

if __name__ == "__main__":
    phrase = "timex watch men"
    products = AmazonSearchUtils.get_search_page_results(phrase, use_cached=True)
    for p in products:
        print p
    #for p in AmazonSearchUtils.sort_by_review_score(products):
    #    print p
    # updated_products = []
    # for product in products:
    #     updated_products.append(get_product_info(product))
    #
    # for p in updated_products:
    #     print p
