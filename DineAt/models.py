import numpy as np
import pandas as pd
from pandas import json_normalize
import requests

def answer(location):
    # location 
    URL = "https://geocode.search.hereapi.com/v1/geocode"
    api_key = 'U3GmE0N3-Hm5gn8CSFsyQ0iPniwSANlhdWUwOG3beAM' # Acquire from developer.here.com
    PARAMS = {'apikey':api_key,'q':location} 
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS) 
    data = r.json()
    #Acquiring the latitude and longitude from JSON 
    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']

    # zomato data

    # credentials
    headers = {'user-key': '7be7bf7032d86c36e0a0ca1d42b92939'}
    # url 
    url = ('https://developers.zomato.com/api/v2.1/search?' + '&start=0&count=20 &lat={}&lon={}&sort= real_distance').format( latitude, longitude)
    # results into a json
    result =  requests.get(url,headers=headers).json()
    venues = result['restaurants']
    venues = json_normalize(venues)

    #selection of hotels
    select = ['restaurant.name','restaurant.url','restaurant.location.address','restaurant.cuisines','restaurant.timings','restaurant.average_cost_for_two','restaurant.user_rating.aggregate_rating','restaurant.photos_url','restaurant.menu_url','restaurant.phone_numbers']
    venues = venues[select]
    venues.columns = venues.columns.str.replace('restaurant.','')
    venues.rename(columns={'location.address':'address','user_rating.aggregate_rating':'rating'},inplace=True)
    venues['rating'] = venues['rating'].astype(float)
    venues['factor'] =  venues['rating'] + venues['average_cost_for_two']
    sort_venues = venues.sort_values(by= 'factor')
    x = sort_venues.iloc[[0,9,10,19]]
    return x