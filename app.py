# Billboard Top 100 Web Scraper by Mik 
# https://github.com/itsnotmik

# Imports
from datetime import date, timedelta                       #for getting today's date
from bs4 import BeautifulSoup as soup           #for souping html
from urllib.request import urlopen as request   #for getting hmtl from site
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

# variables
url = 'https://www.billboard.com/charts/'       #base URL address
hot100 = 'hot-100/'                             #hot 100 URL addition
board_date = date.today() - timedelta(1)        #yesterdays date & holder for date URL addition
    #example URL is URL + HOT100 + BOARD_DATE
    #https://www.billboard.com/charts/hot-100/2023-07-21

client = ''                 #placeholder for client from HTML request
n = 10                      #number of songs to grab (default 10)
json = []

def match_img_class(css_class):
    return css_class is not None and css_class == 'c-lazy-image__img lrv-u-background-color-grey-lightest lrv-u-width-100p lrv-u-display-block lrv-u-height-auto'

def getBB100hot(days):
    json = []
    client = request(url+hot100+str(board_date - timedelta(days))) #grab html from combined URL
    page_html = client.read()                   #read HTML from client  
    client.close()                              #close connection to client
    page_soup = soup(page_html, "html.parser")  #soup html
   
    #grab all h3 tags with class 'a-no-trucate' (this grabs all containers with Song Name inside)
    containers = page_soup.find_all('h3', class_='a-no-trucate')         
    #grab all span tags with class 'a-no-trucate' (this grabs all containers with Artist Name inside)
    a_containers = page_soup.find_all('span', class_='a-no-trucate')
    #grab all div tags with class 'lrv-a-crop-1x1 a-crop-67x100@mobile-max' (this grabs all containers with album img src)
    i_containers = page_soup.find_all('div', class_=match_img_class)

    for i in i_containers:
        if '344x344' not in i.get('data-lazy-src'):
            i_containers.remove(i)
    
    try:
        for c in range(0, n):
            #place song name, artist name, and img src into variables
            song = containers[c].get_text().strip()
            artist = a_containers[c].get_text().strip()
            src = i_containers[c]
            img = src.get('data-lazy-src')

            dic = {'name': song,
                'artist': artist,
                'album': img}

            #print all charting songs to console
            json.append(dic)
    except IndexError:
        print("Index Error - Billboard Hot 100 is not updated for the requested date")
        json_r = getBB100hot(7)
        return json_r

    return json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
@cross_origin()
def returnbb100():
    return jsonify(getBB100hot(0))

if __name__ == '__main__':
    app.run(host='0.0.0.0')