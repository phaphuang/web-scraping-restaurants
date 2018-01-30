#  -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from googleplaces import GooglePlaces, types, lang
import pandas as pd

API_KEY = 'AIzaSyCKxP9RqeiMwqU4lrS0WwNabD55fjs-XHE'

google_places = GooglePlaces(API_KEY)

#query_result = google_places.nearby_search(
#        location='หางดง', keyword='ATM หางดง',
#        radius=10000)
query_result = google_places.radar_search(keyword="ร้านอาหาร", location="เมืองเชียงใหม่", radius=10000)

if query_result.has_attributions:
    print(query_result.html_attributions)

'''
iMaxPlacesToFetch = 1000
iPlacesFetched = 0

res_list = []

while iPlacesFetched < iMaxPlacesToFetch:
    for place in query_result.places:
        place.get_details()
        if place.rating > 3:
            print('[%i] %s %s' % (iPlacesFetched, place.name, place.rating))
            res_list.append([place.name, place.rating])
        iPlacesFetched = iPlacesFetched + 1
    if query_result.has_next_page_token:
        query_result = google_places.nearby_search(pagetoken=query_result.next_page_token)


column_name = ['Restuarant Name', 'Ratings']
df = pd.DataFrame(res_list, columns=column_name)
df.to_csv('ChiangMaiRestuarant1000.csv', encoding='utf-8-sig')
'''

restaurant_list = []

for place in query_result.places:
    #print(place.name)
    #print(place.geo_location)

    # The following method has to make a further API call.
    place.get_details()
    print(place.name)
    print(place.details)
    #print(place.local_phone_number)
    print(place.geo_location)
    #print(place.url)
    #print(place.website)
    print(place.rating)
    print(place.formatted_address)
    restaurant_list.append([place.name, place.local_phone_number, place.website, place.url,
                            place.geo_location["lat"], place.geo_location["lng"], place.rating, place.formatted_address])

column_name = ['ATM Name', 'Phone Number', 'Website', 'Google URL', 'Latitude', 'Longitude', 'Ratings', 'Address']
df = pd.DataFrame(restaurant_list, columns=column_name)
df.to_csv('output/ChiangMaiRestaurantR10000.csv', encoding='utf-8-sig')
