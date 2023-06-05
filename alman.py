import requests
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd


def almanea_scraping(url):
    counter = 0
    file=open('almanea.csv','w',encoding='utf-8',newline='')
    csv_writer=csv.writer(file)
    csv_writer.writerow(['اسم المنتج' ,'الموديل', 'السعر' ,'التوفر','SKU', 'الأبعاد الخارجية' ,'الأبعاد الداخلية','بلد الصنع','لينك المنتج','اسم الموقع'])
    url = "https://almanea.sa/ar/air-conditioning-devices.html?p=1&product_list_limit=all"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    productlink = soup.findAll("li" , class_="item product product-item")
    for ele in productlink:
        name = 'لا يوجد'
        Model='موجود بالاسم'
        price = 'لا يوجد'
        SKU = 'لا يوجد'
        Innerdimension = 'لا يوجد'
        Outerunitdimension = "لا يوجد"
        Avail = 'لا يوجد'
        sitename="المنيع"
        Manufacturer = "لا يوجد"
        href=ele.findNext('a')['href']
        r2=requests.get(href)
        soup2=BeautifulSoup(r2.content,"lxml")
        name =soup2.find('div' , class_="page-title-wrapper product").text
        try:
            try:
                price1=re.findall(r'[\d]+[.,\d]+',soup2.find('div' , class_="product-info-price").find('span', {"data-price-type":"finalPrice"}).text)
                price = price1[0].replace(",","")
            except ValueError:
                price1 = re.findall(r'[\d]+',soup2.find('div' , class_="product-info-price").find('span', {"data-price-type":"finalPrice"}).text)
                price = price1[0].replace(",","")
        except:continue
        try:
            Avail1= soup2.find('div' , class_="stock available").find('span').text
            if Avail1 =="متوفر":
                Avail="نعم"
        except:pass
        SKU=re.findall(r'\d+',soup2.find('div' , class_="product-info-stock-sku").find('div' , class_="value").text)
        Datatable=soup2.find(id="product-attribute-specs-table").findAll('tr')
        for spec in Datatable:
            if spec.findNext('th').text=='أبعاد وجه المكيف (عرض × عمق × إرتفاع)' or spec.findNext('th').text=='أبعاد الوحدة الخارجية (عرض × عمق × إرتفاع)	':
                Outerunitdimension=spec.findNext('th').findNext('td').text
            if spec.findNext('th').text=='أبعاد الوحدة الداخلية (عرض × عمق × إرتفاع)':
                Innerdimension= spec.findNext('th').findNext('td').text
            if spec.findNext('th').text=='بلد الصنع':
                Manufacturer = spec.findNext('th').findNext('td').text
            if 'الموديل' in spec.findNext('th').text:
                Model =spec.findNext('th').findNext('td').text
        csv_writer.writerow(
            [name,Model, price, Avail,SKU[0],Outerunitdimension,Innerdimension,Manufacturer ,href ,sitename])
        print(f"Finishing product Num: {counter}")
        counter+=1
        # if counter == 10:
        #     break
    file.close()
    main_data_frame = pd.read_csv("almanea.csv")
    writer = pd.ExcelWriter(r'almanea_excel_data.xlsx', engine='xlsxwriter')
    main_data_frame.to_excel(writer, index=False)
    writer.close()


almanea_scraping("https://almanea.sa/ar/air-conditioning-devices.html")


