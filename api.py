import requests
import urllib
import pandas as pd
import datetime
import sys

RANKING_CSV_PATH="./ranking_list_{keyword}_{datetime}.csv"
APPLICATION_ID=1019079537947262807

def get_api(url, params):
    result = requests.get(url, params=params)
    if result.status_code == requests.codes.ok:
      return result.json()
    else:
      print("商品名、価格のデータ取得に失敗しました。")
      sys.exit()

def get_item_info(keyword):
  url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
  params = {
    "keyword": keyword,
    "applicationId": APPLICATION_ID,
    "format": "json"
  }
  response = get_api(url, params)
  item_name_list = []
  item_price_list = []
  for item in response["Items"]:
    item_name_list.append(item["Item"]["itemName"])
    item_price_list.append(item["Item"]["itemPrice"])

  for item_name, item_price in zip(item_name_list, item_price_list):
    print(f"商品名:{item_name}, 価格:{item_price}")

  return response

def get_item_min_max_price(keyword):
    url = "https://app.rakuten.co.jp/services/api/Product/Search/20170426"
    params = {
      "keyword": keyword,
      "applicationId": APPLICATION_ID,
      "format": "json"
    }
    response = get_api(url, params)
    item_max_price = []
    item_min_price = []
    for item in response["Products"]:
      item_max_price.append(item["Product"]["maxPrice"])
      item_min_price.append(item["Product"]["minPrice"])
    print(f"最高値:{max(item_max_price)}, 最安値:{min(item_min_price)}")

    return response

def get_item_ranking(keyword):
  url = "https://app.rakuten.co.jp/services/api/IchibaItem/Ranking/20170628"
  params = {
    "keyword": keyword,
    "applicationId": APPLICATION_ID,
    "format": "json"
  }
  response = get_api(url, params)
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
    get_item_info("エアマックス")
    get_item_min_max_price("エアマックス")
    get_item_ranking("エアマックス")

main()