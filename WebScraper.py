#imports
from bs4 import BeautifulSoup
import requests

#ask for input
print("Velden met een '*' zijn verplicht in te vullen!")
print("Anderen kunnen leeg blijven.")
merk = "/" + input('*Merk: ')
model = "/" + input('*Model: ')
postcode = "/" + input('*Postcode: ') + "-"
gemeente = input('*Gemeente: ')

#kmfrom kmto
km = input('Km (j): ')
if km == '' :
    kmFrom = ''
    kmTo = ''
else:
    kmFrom = input('Van: ')
    kmTo = input('Tot: ')
    kmFrom = "kmfrom=" + kmFrom
    kmTo = "&kmto=" + kmTo + "&"

#pricefrom priceto
price = input('price (j): ')
if price == '' :
    priceFrom = ''
    priceTo = ''
else:
    priceFrom = input('Van: ')
    priceTo = input('Tot: ')
    priceFrom = "&pricefrom=" + priceFrom
    priceTo = "&priceto=" + priceTo

print()


url = (f"https://www.autoscout24.be/nl/lst{merk}{model}{postcode}{gemeente}?{kmFrom}{kmTo}sort=standard&desc=0&cy=B&atype=C&ustate=N%2CU&powertype=kw{priceFrom}{priceTo}")
print("Link zoekertjes:")
print(url)
print()

#add website to soup
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#pages checker
try:
    #find last page
    page_number = soup.find_all("li", {"class": "css-1hz8gr1"})[0].get_text()
except:
    page_number = 1

#variables
all_cars = []
all_prices = []
all_mileages = []
all_links = []

#check if page number is 1
if page_number == 1:
    
    #find all cars
    cars = soup.find_all("h2", {"class": "css-4u347z"})

    #find all cars as strings
    cars_str = []
    prices_str = []
    mileages_str = []
    links_str = []
    counter = 0
    for item in cars:
        item = soup.find_all("h2", {"class": "css-4u347z"})[counter].get_text()
        item2 = soup.find_all("span", {"class": ["css-1b5kt8d", "css-125hq55"]})[counter].get_text()
        item3 = soup.find_all("span", {"type": "mileage"})[counter].get_text()
        item4 = soup.find_all("a", {"class": ["emtvtq412", "css-5n6fy4", "e1q3laaa0"]})
        for link in item4:
            link_item = link.get('href')
            links_str.append(link_item)
        cars_str.append(item)
        prices_str.append(item2)
        mileages_str.append(item3)
        counter += 1

    all_cars.extend(cars_str)
    all_prices.extend(prices_str)
    all_mileages.extend(mileages_str)
    all_links.extend(links_str)

else:  
    #find cars
    for i in range(1, int(page_number) + 1):
        #add website to soup
        url = url + "&page=" + str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        #find all cars
        cars = soup.find_all("h2", {"class": "css-4u347z"})

        #find all cars as strings
        cars_str = []
        prices_str = []
        mileages_str = []
        links_str = []
        counter = 0
        for item in cars:
            item = soup.find_all("h2", {"class": "css-4u347z"})[counter].get_text()
            item2 = soup.find_all("span", {"class": ["css-1b5kt8d", "css-125hq55"]})[counter].get_text()
            item3 = soup.find_all("span", {"type": "mileage"})[counter].get_text()
            item4 = soup.find_all("a", {"class": ["emtvtq412 css-5n6fy4 e1q3laaa0"]})
            for link in item4:
                link_item = link.get('href')
                links_str.append(link_item)
            cars_str.append(item)
            prices_str.append(item2)
            mileages_str.append(item3)
            counter += 1

        all_cars.extend(cars_str)
        all_prices.extend(prices_str)
        all_mileages.extend(mileages_str)
        all_links.extend(links_str)

        i += 1

#output
print(len(all_cars), "resultaten gevonden.")
print()

for i in range(0, len(all_cars)):
    index = all_prices[i].find(",")
    print(str(i + 1) + ":", all_prices[i][0:index], all_mileages[i])
    i += 1;

while True:
    id = input("Bekijk: ")

    if id == "":
        break
    else:
        print("https://www.autoscout24.be/" + all_links[int(id)-1])
