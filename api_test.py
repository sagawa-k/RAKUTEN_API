from api import *
import pprint
import pandas as pd

def test_get_item_info():
  res = get_item_info("マグカップ")

  assert len(res["Items"]) >= 1
  assert res["Items"][0]["Item"]["itemName"]
  assert res["Items"][0]["Item"]["itemPrice"]

def test_get_item_min_max_price():
  res = get_item_min_max_price("マグカップ")

  assert len(res["Products"]) >= 1
  assert res["Products"][0]["Product"]["maxPrice"]
  assert res["Products"][0]["Product"]["minPrice"]

def test_get_item_ranking():
  res = get_item_ranking("マグカップ")

  assert len(res["Items"]) >= 1
  assert res["Items"][0]["Item"]["rank"]
  assert res["Items"][0]["Item"]["itemName"]
  assert res["Items"][0]["Item"]["itemPrice"]