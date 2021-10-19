'''
Hello guys ,this code allows you to parse websites(not all,but most of them) with lib requestes and BeautifulSoup
You can try by yourself ,just need to know HMTL,CSS and can read websites's code,
'''

import json
from bs4 import BeautifulSoup
import requests

def get_data():

	headers = {
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
	}
	url = 'https://www.sulpak.kz/f/smartfoniy' #enter url
	answersR = requests.get(url=url,headers=headers)
	s = BeautifulSoup(answersR.text,'lxml')
	pages_number = int(s.find('div',class_='pages-list').find_all('a')[-1].text) #getting pages sum
	res = []                   #List for saving all devices
	for page in range(1,pages_number + 1 ):
		url = f'https://www.sulpak.kz/f/smartfoniy?selectedAvailabilitiesTokens=Availability?page={page}'
		answers = requests.get(url=url,headers=headers)
		s = BeautifulSoup(answers.text,'lxml')
		gadjet_items = s.find('ul',class_='goods-container').find_all('div',class_='product-container-right-side')  #Finding things that we need
		for gj in gadjet_items:
			gadjet_data = gj.find_all('a')
			try:
				gadjet_name = gadjet_data[0].text.strip()     #I find phone's name
			except:    #if we cant find them just write that it doesnot exist
				gadjet_name = 'There is no phone'
			try:
				gadjet_oldprice = gj.find('div',class_='old-price').text.strip().replace('Цена:','')
				gadjet_oldprice = gj.find('div',class_='price').text.strip().replace('Цена:','')
			except:
				gadjet_oldprice = gj.find('div',class_='price').text.strip().replace('Цена:','')

			try:
				gadjet_url = 'https://www.sulpak.kz' + gadjet_data[0].get('href')
			except:
				gadjet_url = 'netu'

			res.append(
				{
					"Имя смартфона":gadjet_name,
					"Цена смартфона":gadjet_oldprice,
					"Ссылка" :gadjet_url

				}
			)

		print(f"Succesfully parsed {page}/{pages_number}")  #we will receive message every time when it parsed
	with open("sulpak.json", "w",newline='',encoding='utf-8') as f:         #Saving our result in JSON
		json.dump(res, f, indent=3, ensure_ascii=False)
def main():
	get_data()
	print('Succesfully parsed')


if __name__== "__main__":
	main()