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

def decode_url(encoded):
    def get_offset(n):
        if 97 <= n <= 122:
            return n - 61
        if 65 <= n <= 90:
            return n - 55
        if 48 <= n <= 71:
            return n - 48
        return -1

    h = {
        '': [
            '&', '=', 'p', '6', '?', 'H', '%', 'B', '.com', 'k', '9', '.html',
            'n', 'M', 'r', 'www.', 'h', 'b', 't', 'a', '0', '/', 'd', 'O', 'j',
            'http://', '_', 'L', 'i', 'f', '1', 'e', '-', '2', '.', 'N', 'm',
            'A', 'l', '4', 'R', 'C', 'y', 'S', 'o', '+', '7', 'I', '3', 'c',
            '5', 'u', 0, 'T', 'v', 's', 'w', '8', 'P', 0, 'g', 0
        ],
        'q': [
            0, '__3F__', 0, 'Photos', 0, 'https://', '.edu', '*', 'Y', '>', 0,
            0, 0, 0, 0, 0, '`', '__2D__', 'X', '<', 'slot', 0, 'ShowUrl',
            'Owners', 0, '[', 'q', 0, 'MemberProfile', 0, 'ShowUserReviews',
            '"', 'Hotel', 0, 0, 'Expedia', 'Vacation', 'Discount', 0,
            'UserReview', 'Thumbnail', 0, '__2F__', 'Inspiration', 'V', 'Map',
            ':', '@', 0, 'F', 'help', 0, 0, 'Rental', 0, 'Picture', 0, 0, 0,
            'hotels', 0, 'ftp://'
        ],
        'x': [
            0, 0, 'J', 0, 0, 'Z', 0, 0, 0, ';', 0, 'Text', 0, '(', 'x',
            'GenericAds', 'U', 0, 'careers', 0, 0, 0, 'D', 0, 'members',
            'Search', 0, 0, 0, 'Post', 0, 0, 0, 'Q', 0, '$', 0, 'K', 0, 'W', 0,
            'Reviews', 0, ',', '__2E__', 0, 0, 0, 0, 0, 0, 0, '{', '}', 0,
            'Cheap', ')', 0, 0, 0, '#', '.org'
        ],
        'z': [
            0, 'Hotels', 0, 0, 'Icon', 0, 0, 0, 0, '.net', 0, 0, 'z', 0, 0,
            'pages', 0, 'geo', 0, 0, 0, 'cnt', '~', 0, 0, ']', '|', 0,
            'tripadvisor', 'Images', 'BookingBuddy', 0, 'Commerce', 0, 0,
            'partnerKey', 0, 'area', 0, 'Deals', 'from', '\\', 0, 'urlKey', 0,
            '\'', 0, 'WeatherUnderground', 0, 'MemberSign', 'Maps', 0, 'matchID',
            'Packages', 'E', 'Amenities', 'Travel', '.htm', 0, '!', '^', 'G'
        ]
    }

    decoded = ''
    i = 0
    while i < len(encoded):
        j = encoded[i]
        f = j
        if h.get(j) and i + 1 < len(encoded):
            i += 1
            f += encoded[i]
        else:
            j = ''
        g = get_offset(ord(encoded[i]))
        if g < 0 or type(h[j][g]) == 'str':
            decoded += f
        else:
            decoded += h[j][g]
        i += 1

    decoded = decoded.replace('__', '').replace('%253A', ':')
    decoded = re.sub(r'.*?(http.*?)-a_url.*', r'\1', decoded)
    decoded = re.sub(r'5F5F([A-Z\d]{2})5F5F',
        lambda match: chr(int(match.group(1), 16)), decoded)

    return decoded

def main():
    restaurants = []

    dl_page_src(base_url + location_url)

    with open('tripadvisor_chiangmai_restaurant.html', encoding='utf-8') as page_src:
        source = page_src.read()

    soup = BeautifulSoup(source, 'html.parser')

    # get last element in the pagenation (i.e.: total number of pages)
    page_count = int(soup.select('.pagination a')[-1].text.strip())
    for page_no in range(page_count):
        if(int(page_no) % 3 == 0):
            time.sleep(10)
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
            try:
                rating = result.select_one('div.rating span.ui_bubble_rating')['alt'].split(" ")[0]
            except:
                rating = 'NaN'
            #print(rating)

            total_reviews = result.select('div.rating span.reviewCount a')[0].text.strip().replace(' reviews', '')
            #print(total_reviews)

            review_url = ta_url + result.select('a.property_title')[0]['href']

            # get image url
            try:
                image_url = result.select_one('.photo_booking a div img')['src']
            except:
                image_url = 'static/images/generic.jpg'
            #print(image_url)

            ###########################################
            ### Scraping information in review page ###
            ###########################################
            dl_review_page_src(review_url)
            with open('tripadvisor_chiangmai_restaurant_review.html', encoding='utf-8') as page_src:
                review_page = page_src.read()
            #response = requests.get(review_url, headers=headers)
            #rp = BeautifulSoup(response.content, 'html.parser')
            rp = BeautifulSoup(review_page, 'html.parser')

            # get address in review page
            try:
                street = rp.select('.address span.street-address')[0].text.strip()
            except:
                street = 'NaN'
            #print(street)
            try:
                more_info = rp.select('.address span.extended-address')[0].text.strip()
                #print(more_info)
            except:
                more_info = 'NaN'
            try:
                province = ' '.join(rp.select('.address span.locality')[0].text.strip().replace(',', '').split(' ')[:-1])
            except:
                province = 'NaN'
            #print(province)
            try:
                zipcode = rp.select('.address span.locality')[0].text.strip().replace(',', '').split(' ')[-1]
            except:
                zipcode = 'NaN'
            #print(zipcode)

            # get phone info in review page
            try:
                phone = rp.select('.indirectContactInfo')[0].attrs['data-phonenumber']
            except:
                phone = 'NaN'
            #print(phone)

            # get open-close timeline range
            try:
                dayRange = rp.select('.dayRange')[0].text.strip()
            except:
                dayRange = 'NaN'
            try:
                timeRange = rp.select('.timeRange')[0].text.strip()
            except:
                timeRange = 'NaN'
            #print(dayRange, timeRange)

            # get cuisines' tags
            try:
                tags = rp.select('.cuisines div.text')[0].attrs['data-content']
            except:
                tags = 'NaN'
            #print(tags)

            # get website url
            try:
                raw_website = rp.select('.website')[0].attrs['data-ahref']
                website = decode_url(raw_website)
                #print(website)
            except:
                website = 'NaN'

            # get all image url in review page
            image_list = []
            check_noscript_img = rp.select('.prw_common_location_photos span.imgWrap noscript img')
            if not check_noscript_img:
                lazy_load_objs1 = rp.select('.prw_common_location_photos span.imgWrap img')
            else:
                lazy_load_objs1 = check_noscript_img
            for lazy_load_obj in lazy_load_objs1:
                image_list.append(lazy_load_obj['src'])
            lazy_load_objs2 = rp.select('.ppr_priv_two_photos span.imgWrap noscript img')
            for lazy_load_obj in lazy_load_objs2:
                image_list.append(lazy_load_obj['src'])
            #print(image_list)

            restaurants.append([title, rating, total_reviews, review_url, image_url, street, more_info, province, zipcode, phone, dayRange, timeRange, tags, image_list])

        # compute the url for the next page
        next_page = base_url + 'oa' + str((page_no + 1) * 30) + '-' + location_url

        time.sleep(15)
        dl_page_src(next_page)

        with open('tripadvisor_chiangmai_restaurant.html', encoding='utf-8') as page_src:
            source = page_src.read()

        soup = BeautifulSoup(source, 'html.parser')

    column_name = ['Restaurant Name', 'Ratings', 'No of Reviews', 'Review URL', 'Image URL', 'Street', 'More Info', 'Province', 'Zipcode', 'Phone Number', 'Day Open', 'Time Open', 'Tags', 'Other Image URL']
    df = pd.DataFrame(restaurants, columns=column_name)
    df.to_csv('output/TripadvisorChiangMaiRestaurant.csv', encoding='utf-8-sig')

def dl_page_src(url):
    print(url)
    # Create a session
    response = requests.Session()

    # Create adapters with the retry logic for each
    http = requests.adapters.HTTPAdapter(max_retries=10)
    https = requests.adapters.HTTPAdapter(max_retries=10)

    # Replace the session's original adapters
    response.mount('http://', http)
    response.mount('https://', https)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    with open('tripadvisor_chiangmai_restaurant.html', 'w', encoding='utf-8') as saved_page:
        saved_page.write(soup.prettify(encoding='utf-8').decode('utf-8'))

def dl_review_page_src(url):
    print(url)
    # Create a session
    response = requests.Session()

    # Create adapters with the retry logic for each
    http = requests.adapters.HTTPAdapter(max_retries=10)
    https = requests.adapters.HTTPAdapter(max_retries=10)

    # Replace the session's original adapters
    response.mount('http://', http)
    response.mount('https://', https)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    with open('tripadvisor_chiangmai_restaurant_review.html', 'w', encoding='utf-8') as saved_page:
        saved_page.write(soup.prettify(encoding='utf-8').decode('utf-8'))

if __name__ == '__main__':
    main()
