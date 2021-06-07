import requests
import urllib
import pandas as pd
import datetime

RANKING_CSV_PATH="./ranking_list_{keyword}_{datetime}.csv"

def get_api(url):
    result = requests.get(url)
    return result.json()

def get_item_info(keyword):
  url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&keyword={keyword}&applicationId=1019079537947262807"
  response = get_api(url)
  item_name_list = []
  item_price_list = []
  for item in response["Items"]:
    item_name_list.append(item["Item"]["itemName"])
    item_price_list.append(item["Item"]["itemPrice"])

  for item_name, item_price in zip(item_name_list, item_price_list):
    print(f"商品名:{item_name}, 価格:{item_price}")
  
  return response

def get_item_min_max_price(keyword):
    url = f"https://app.rakuten.co.jp/services/api/Product/Search/20170426?applicationId=1019079537947262807&format=json&keyword={keyword}"
    response = get_api(url)
    item_max_price = []
    item_min_price = []
    for item in response["Products"]:
      item_max_price.append(item["Product"]["maxPrice"])
      item_min_price.append(item["Product"]["minPrice"])
    print(f"最高値:{max(item_max_price)}, 最安値:{min(item_min_price)}")

    return response

def get_item_ranking(keyword):
  url = f"https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628?applicationId=1019079537947262807&format=json&keyword={keyword}"
  response = get_api(url)
  item_rank = []
  item_name_list = []
  item_price_list = []
  for item in response["Items"]:
    item_rank.append(item["Item"]["rank"])
    item_name_list.append(item["Item"]["itemName"])
    item_price_list.append(item["Item"]["itemPrice"])

  now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
  df = pd.DataFrame({"ランキング":item_rank, "商品名":item_name_list, "価格":item_price_list })
  df.to_csv(RANKING_CSV_PATH.format(keyword=keyword, datetime=now), encoding="utf-8-sig")

  return response

def main():
    get_item_info("マグカップ")
    get_item_min_max_price("マグカップ")
    get_item_ranking("マグカップ")

main()