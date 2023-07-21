# Billboard Top 100 Web Scraper by Mik 
# https://github.com/itsnotmik

# Imports
from datetime import date                       #for getting today's date
from bs4 import BeautifulSoup as soup           #for souping html
from urllib.request import urlopen as request   #for getting hmtl from site

# variables
url = 'https://www.billboard.com/charts/'       #base URL address
hot100 = 'hot-100/'                             #hot 100 URL addition
bill200 = 'billboard-200/'                      #billboard 200 URL addition
glob200 = 'billboard-global-200/'               #global 200 URL addition
board_date = date.today()                       #todays date & holder for date URL addition
    #example URL is URL + HOT100 + BOARD_DATE
    #https://www.billboard.com/charts/hot-100/2023-07-21

client = ''                 #placeholder for client from HTML request
source = 'hot_100'          #placeholder for source of scraping (used in csv file naming)
n = 10                      #number of songs to grab (default 10)
csv = False                 #write to csv (default False)

# print banner
print("""\
  ___ ___ __ __    __          _______ __ __ __ __                        __    _______                _____ _______ _______    ___ ___       __       _______                                  
 |   Y   |__|  |--|  .-----.  |   _   |__|  |  |  |--.-----.---.-.----.--|  |  |       .-----.-----.  | _   |   _   |   _   |  |   Y   .-----|  |--.  |   _   .----.----.---.-.-----.-----.----.
 |.      |  |    < |_|__ --|  |.  1   |  |  |  |  _  |  _  |  _  |   _|  _  |  |.|   | |  _  |  _  |  |.|   |.  |   |.  |   |  |.  |   |  -__|  _  |  |   1___|  __|   _|  _  |  _  |  -__|   _|
 |. \_/  |__|__|__|  |_____|  |.  _   |__|__|__|_____|_____|___._|__| |_____|  `-|.  |-|_____|   __|  `-|.  |.  |   |.  |   |  |. / \  |_____|_____|  |____   |____|__| |___._|   __|_____|__|  
 |:  |   |                    |:  1    \                                         |:  |       |__|       |:  |:  1   |:  1   |  |:      |              |:  1   |               |__|              
 |::.|:. |                    |::.. .  /                                         |::.|                  |::.|::.. . |::.. . |  |::.|:. |              |::.. . |                                 
 `--- ---'                    `-------'                                          `---'                  `---`-------`-------'  `--- ---'              `-------'
""")

# get date for billboard search
while True:
    day = input('Which day would like to search the charts:\n'
                '(Today or YYYY-MM-DD format): ')
    
    #check if today is entered
    if day.lower() == 'today': 
        #if it is, put todays date in board_date
        board_date = date.today()
        break
    #check if entered date is in correct format
    elif day[:3].isnumeric() and day[4] == '-' and day[5:6].isnumeric() and day[7] == '-' and day[8:9].isnumeric():
        #if it is formatted correctly, verify the date is not outside of range of Billboard charts
        if day < '2020-09-19' or day > str(date.today()):
            print('Date entered is before 2020-09-19 or in the future\n')
        else:
            print()
            #assign entered date as board_date
            board_date = day
            break

# print board selection text
print('Select the chart you want:\n'
      '1. Hot 100\n'
      '2. Billboard 200\n'
      '3. Global 200\n')

while True:
    selection = input('Input 1, 2, or 3: ')
    
    if selection == '1':
        print('Grabbing Billboard Hot 100\n')
        client = request(url+hot100+str(board_date)) #grab html from combined URL
        break
    elif selection == '2':
        print('Grabbing Billboard 200\n')
        client = request(url+bill200+str(board_date)) #grab html from combined URL
        source = '200'
        break
    elif selection == '3':
        print('Grabbing Billboard Global 200\n')
        client = request(url+glob200+str(board_date)) #grab html from combined URL
        source = 'global_200'
        break
    else:
        print('Incorrect Input\n')

page_html = client.read()                   #read HTML from client  
client.close()                              #close connection to client
page_soup = soup(page_html, "html.parser")  #soup html

while True: #check if user wants CSV to be created
    selection = input('Would you like the data saved in a CSV file (yes or no): ')

    if selection.lower() == 'yes' or selection.lower() == 'y':
        print()
        csv = True
        break
    elif selection.lower() == 'no' or selection.lower() == 'n':
        print()
        break
    else:
        print('Please enter yes or no\n')

while True: #check how many outputs the user wants
    num = int(input('How many outputs do you want (<100): '))
    
    if num > 100 or num < 1:
        print('Number can not exceed 100 or be less than 1\n')
    else:
        print()
        n = num
        break
    
#grab all h3 tags with class 'a-no-trucate' (this grabs all containers with Song Name inside)
containers = page_soup.find_all('h3', class_='a-no-trucate')         
#grab all span tags with class 'a-no-trucate' (this grabs all containers with Artist Name inside)
a_containers = page_soup.find_all('span', class_='a-no-trucate')
#grab all div tags with class 'lrv-a-crop-1x1 a-crop-67x100@mobile-max' (this grabs all containers with album img src)
i_containers = page_soup.find_all('div', class_='lrv-a-crop-1x1 a-crop-67x100@mobile-max')

if csv: #if CSV file is wanted, create CSV based on chart selected and date
    today = date.today()

    filename = 'billboard_' + source + '_(' + str(board_date) + ').csv'
    f = open(filename, 'w')

    headers = 'Song, Artist, Album Image Source\n'
    f.write(headers)

for c in range(0, n):
    #place song name, artist name, and img src into variables
    song = containers[c].get_text().strip()
    artist = a_containers[c].get_text().strip()
    src = i_containers[c].findAll('img')
    img = src[0].get('data-lazy-src')

    #print all charting songs to console
    print(str(c+1) + ') ' + song + ' by ' + artist)

    if csv: #write data to CSV file
        f.write('\"' + song + '\", ' + '\"' + artist.replace('Featuring', 'Feat.') + '\", ' + '\"' + img + '\"\n')

print('\n\n=^..^=   =^..^=   =^..^=    =^..^=    =^..^=    =^..^=    =^..^=   =^..^=\n'
      '    Thank you for checking out Mik\'s Billboard Top Charts Web Scraper\n\n')
