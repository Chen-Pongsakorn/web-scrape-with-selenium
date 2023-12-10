import argparse
import traceback
from service.compare_goods import start_comparing, get_main_goods
from utils.json_utils import read_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--total_goods", type=int, required=True)
    args = parser.parse_args()
    total_goods = args.total_goods

    if total_goods:
        config = read_json("./config/config.json")
        if config:
            try:
                start_comparing(config, total_goods)
            except Exception as e:
                traceback_string = traceback.format_exc()
                print(traceback_string)
                print(e)