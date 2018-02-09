import gmaps
import gmaps.datasets
from ipywidgets.embed import embed_minimal_html
import pandas as pd

gmaps.configure(api_key='AIzaSyCKxP9RqeiMwqU4lrS0WwNabD55fjs-XHE') # Fill in with your API key

#marker_locations = [
#    (-34.0, -59.166672),
#    (-32.23333, -64.433327),
#    (40.166672, 44.133331),
#    (51.216671, 5.0833302),
#    (51.333328, 4.25)
#]
df = pd.read_csv('output/UpdateTripadvisorRestaurantLocation.csv', encoding='ISO-8859-1')
df.dropna(axis=0, inplace=True)
marker_locations = [(lat, lng) for lat, lng in zip(df['Latitude'], df['Longitude'])]
#print(marker_locations)

fig = gmaps.figure(center=(18.785585, 98.981766), zoom_level=13)
markers = gmaps.marker_layer(marker_locations)
fig.add_layer(markers)
embed_minimal_html('output/export.html', views=[fig])
