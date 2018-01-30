from bs4 import BeautifulSoup
import json
import requests
import re
import time
import pandas as pd

user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

ta_url = 'http://www.tripadvisor.com'
base_url = 'http://www.tripadvisor.com/Restaurants-g293917-'
location_url = 'Chiang_Mai.html'

def main():
    restaurants = []

    dl_page_src(base_url + location_url)

    with open('tripadvisor.html', encoding='utf-8') as page_src:
        source = page_src.read()

    soup = BeautifulSoup(source, 'html.parser')

    # get last element in the pagenation (i.e.: total number of pages)
    page_count = int(soup.select('.pagination a')[-1].text.strip())
    for page_no in range(page_count):
        # our formula to compute the next url to download:
        # [page_no * 30]
        # page 1: base_url + location_url
        # page 2: base_url + 'oa' + [page_no * 30] + '-' + location_url
        # etc ...
        page_results = soup.select('#EATERY_LIST_CONTENTS .listing')
        #print(page_results)

        # loop over all elements and extract the useful data
        for result in page_results:
            title = result.select('.title a')[0].text.strip()
            #print(title)
            rating = result.select_one('div.rating span.ui_bubble_rating')['alt'].split(" ")[0]
            #print(rating)

            total_reviews = result.select('div.rating span.reviewCount a')[0].text.strip().replace(' reviews', '')
            #print(total_reviews)

            review_url = ta_url + result.select('a.property_title')[0]['href']

            #print("Rating: " + rating + ", Reviews: " + review_url)

            # get image url
            try:
                image_url = result.select_one('.photo_booking a div img')['src']
            except:
                image_url = 'static/images/generic.jpg'
            #print(image_url)

            restaurants.append([title, rating, total_reviews, review_url, image_url])

        # compute the url for the next page
        next_page = base_url + 'oa' + str((page_no + 1) * 30) + '-' + location_url

        time.sleep(15)
        dl_page_src(next_page)

        with open('tripadvisor_chiangmai_restaurant.html', encoding='utf-8') as page_src:
            source = page_src.read()

        soup = BeautifulSoup(source, 'html.parser')

    #with open('chiangmai_restaurant.json', 'w', encoding='utf-8') as output:
    #    output.write(json.dumps(restaurants, indent=4))

    column_name = ['Restaurant Name', 'Ratings', 'No of Reviews', 'Review URL', 'Image URL']
    df = pd.DataFrame(restaurants, columns=column_name)
    df.to_csv('output/TripadvisorChiangMaiRestaurant.csv', encoding='utf-8-sig')

def dl_page_src(url):
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    with open('tripadvisor_chiangmai_restaurant.html', 'w', encoding='utf-8') as saved_page:
        saved_page.write(soup.prettify(encoding='utf-8').decode('utf-8'))

if __name__ == '__main__':
    main()
