from utils.scrape import Scrape
from utils.json_utils import write_json

def transform_main_result(main_good_result, shop_name):
    dict_of_goods = {}
    for item in main_good_result:
        if item.startswith('฿'):
            if product_name:
                data_price = {
                    "shop_name": shop_name,
                    "price": float(item.replace('฿', '').replace(',', ''))
                }
                if len(dict_of_goods[product_name]):
                    if data_price["price"] < dict_of_goods[product_name][0]["price"]:
                        dict_of_goods[product_name][0]["price"] = data_price["price"]
                else:
                    dict_of_goods[product_name].append(data_price)
        else:
            product_name = item
            dict_of_goods[item] = []

    return dict_of_goods

def get_main_goods(config=None, total_goods=1, scroll_down_times=1):
    main_goods_result = {}
    while len(main_goods_result) < total_goods:
        if config:
            find_element_step = [
                {
                    "element": None,
                    "output": "scroll_down",
                    "key_value": None,
                    "scroll_down_by": 1080,
                    "scroll_down_times": scroll_down_times
                },
                {
                    "element": "//div[@id='product-list']",
                    "output": "text",
                    "key_value": None,
                    "scroll_down_by": None,
                    "scroll_down_times": None
                }
            ]
            main_goods_result = Scrape(url=config["lotuss_target_goods_url"]).find_element(find_element_step)
            main_goods_result = (main_goods_result[1]["text_result"]).split("\n")
            main_goods_result = transform_main_result(main_goods_result, "lotus")
            scroll_down_times += 10

    return main_goods_result


def transform_search_result(search_goods_result):
    dict_result = {}
    for order, item in enumerate(search_goods_result, start=0):
        if order == 2:
            dict_result["product_name"] = item["text_result"]
        elif order == 3:
            dict_result["shop_name"] = item["text_result"]
        elif order == 4:
            dict_result["price"] = float(item["text_result"].replace('฿', '').replace(',', ''))

    return dict_result


def get_lazada_search_result(config=None, search_value=None):
    find_element_step = [
        {
            "element": "//input[@id='q']",
            "output": "search",
            "key_value": search_value,
            "scroll_down_by": None,
            "scroll_down_times": None
        },
        {
            "element": "//img[@class='jBwCF '][1]",
            "output": "click",
            "key_value": None,
            "scroll_down_by": None,
            "scroll_down_times": None
        },
        {
            "element": "//h1[@class='pdp-mod-product-badge-title'][1]",
            "output": "text",
            "key_value": None,
            "scroll_down_by": None,
            "scroll_down_times": None
        },
        {
            "element": "//a[@class='pdp-link pdp-link_size_l pdp-link_theme_black seller-name__detail-name'][1]",
            "output": "text",
            "key_value": None,
            "scroll_down_by": None,
            "scroll_down_times": None
        },
        {
            "element": "//span[@class='pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'][1]",
            "output": "text",
            "key_value": None,
            "scroll_down_by": None,
            "scroll_down_times": None
        }
    ]
    search_goods_result = Scrape(url=config).find_element(find_element_step)
    search_goods_result = transform_search_result(search_goods_result)

    return search_goods_result


def get_search_result(config=None, search_value=None):
    search_goods_result = []
    for order, key in enumerate(config, start=0):
        if "lazada" in config:
            result_lazada = get_lazada_search_result(config[key], search_value)
            search_goods_result.append(result_lazada)

    return search_goods_result


def get_price(item):
    return item['price']


def start_comparing(config=None, total_goods=None):
    dict_compared_result = {}
    dict_main_goods = get_main_goods(config, total_goods)
    for order, key in enumerate(dict_main_goods, start=1):
        print(order)
        list_all_goods_detail = []
        search_result = get_search_result(config["dict_compared_url"], key)
        list_all_goods_detail += search_result
        list_all_goods_detail += [
            {
            "product_name": key,
            "shop_name": dict_main_goods[key][0]["shop_name"],
            "price": dict_main_goods[key][0]["price"]
        }
        ]
        print(list_all_goods_detail)
        dict_compared_result[order] = {
            "top_pirce": max(list_all_goods_detail, key=get_price),
            "lowest_price": min(list_all_goods_detail, key=get_price),
            "all_goods_details": list_all_goods_detail
        }
        break

    write_json(dict_compared_result, 'output/result.json')
    
    return dict_compared_result