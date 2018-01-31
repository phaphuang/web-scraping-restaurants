'''
author: Karl Thornton <karl.genockey.thornton@gmail.com>
Implementation of tripadvisor's asdf "de-obfuscation" javascript
function in Python
https://kaijento.github.io/2017/03/17/web-scraping-tripadvisor.com/
'''

import re, requests

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

if __name__ == '__main__':
    url  = 'https://www.tripadvisor.fr/Restaurant_Review-g187147-d9750183-Reviews-Restaurant_H-Paris_Ile_de_France.html'
    r    = requests.get(url, headers={'user-agent': 'Mozilla/5.0'})

    #email      = re.search(r'ta\.locationDetail\.checkEmailAction.+\'(.+)\'', r.text).group(1)
    #obfuscated = re.search(r'\{\'aHref\':\'([^\']+)', r.text).group(1)

    #print(email)
    print(decode_url("PFnJTVMVIGJJCJiJC8L"))
