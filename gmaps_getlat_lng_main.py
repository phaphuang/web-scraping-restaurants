import googlemaps
import pandas as pd

def get_latitude(address):
    try:
        gmaps = googlemaps.Client(API_KEY)
        #address = "Mr KAI Restaurant"
        geocode_result = gmaps.geocode(address + ' Chiang Mai')
        print(geocode_result[0]['geometry']['location']['lat'])
        #print(geocode_result[0]['geometry']['location']['lat'])
        return geocode_result[0]['geometry']['location']['lat']
    except:
        return "NaN"

def get_longitude(address):
    try:
        gmaps = googlemaps.Client(API_KEY)
        #address = "Mr KAI Restaurant"
        geocode_result = gmaps.geocode(address + ' Chiang Mai')
        #print(geocode_result[0]["geometry"])
        print(geocode_result[0]['geometry']['location']['lng'])
        return geocode_result[0]['geometry']['location']['lng']
    except:
        return "NaN"

API_KEY = 'AIzaSyCKxP9RqeiMwqU4lrS0WwNabD55fjs-XHE'

df = pd.read_csv('output/TripadvisorChiangMaiRestaurant.csv')
#df = pd.read_csv('temp.csv', encoding='utf-8')
print(df)

#print(df)

df['Latitude'] = df['Restaurant Name'].apply(get_latitude)
df['Longitude'] = df['Restaurant Name'].apply(get_longitude)
print(df)

df.to_csv('output/UpdateTripadvisorRestaurantLocation.csv')#, encoding='utf-8-sig')
