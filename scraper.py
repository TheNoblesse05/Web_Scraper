from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq 

my_url = 'https://www.newegg.com/p/pl?d=graphics+card&N=100006662'

#opening connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,'html.parser') 

print(page_soup.h1)
print(page_soup.body.span)

#grabs every product
containers = page_soup.findAll('div',{'class':'item-container'})
print(len(containers))

#creating the csv file
f = open('graphics_card.csv','w')
header = 'Company,Product Name,Price,Shipping\n'
f.write(header)

for i in range(4,len(containers)):
	container = containers[i]
	#getting the name of the company
	tag1 = container.findAll('div',{'class':'item-branding'})
	company = tag1[0].a.img['title']
	print(company)
	#getting the product name
	tag2 = container.findAll('a',{'class':'item-title'})
	prod_name = tag2[0].text
	print(prod_name)
	#getting the pirce
	try:
		tag4 = container.findAll('strong',{'class':'item-buying-choices-price'})
		price = tag4[0].text
		print(price)
	except:
		try:
			tag4 = container.findAll('li',{'class':'price-current'})
			price = tag4[0].strong.text
			price = '$'+ price + tag4[0].sup.text
			print(price)
		except:
			price = 'Not Available'
	#getting the shipping details
	tag3 = container.findAll('li',{'class':'price-ship'})
	shipping = tag3[0].text.strip()
	print(shipping)
	#writing to our csv file
	f.write(company+','+prod_name.replace(',','|')+','+price.replace(',','')+','+shipping+'\n')	
f.close()