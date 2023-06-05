
from info import *
def blackbox_scraping(url):
    linkat=[]
    r= requests.get(url)
    soup = BeautifulSoup(r.content ,"lxml")

    linksbox=soup.find("ol" , class_="products list items product-items").findAll("li" , class_="item product product-item")
    file = open('blackbox.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    csv_writer.writerow(
        ['اسم المنتج','الموديل' , 'السعر', 'التوفر', 'SKU', 'الأبعاد الخارجية', 'الأبعاد الداخلية', 'بلد الصنع', 'لينك المنتج','اسم الموقع'])
    for ele1 in linksbox:
        href = ele1.find('a')['href']
        linkat.append(href)
    counter =0
    for ele2 in linkat:
        counter+=1
        print(f"We are in link {counter}")
        productlink=ele2
        name = 'لا يوجد'
        Model="موجود بالاسم"
        price = 'لا يوجد'
        SKU = 'لا يوجد'
        Innerdimension = 'لا يوجد'
        Outerunitdimension = "لا يوجد"
        Avail = 'لا يوجد'
        Manufacturer = "لا يوجد"
        sitename = "الصندوق الأسود"
        r2=requests.get(ele2)
        soup2=BeautifulSoup(r2.content , "lxml")
        name = soup2.find("h1" , class_="page-title").text
        # try:
        #     Model=re.findall(r'(?<=-).*' , name)[0].strip()
        # except:pass
        try:
            Avail1 = soup2.find("div",class_="stock available").find("span").text
            if Avail1 =="متوفر في المخزن":
                Avail="نعم"
        except:pass
        try:
            Datatable=soup2.find("table" , id="product-attribute-specs-table").find("tbody").findAll("tr")
            for ele3 in Datatable:
                if ele3.find("th").text=="SKU":
                    SKU=re.findall(r'\d+',ele3.find("td").text)
                if ele3.find("th").text=="بلد الصنع":
                    Manufacturer=ele3.find("td").text
                if ele3.find("th").text=="الموديل":
                    Model=ele3.find("td").text
        except:pass
        try:
            try:
                price1 = re.findall(r'[\d]+[.,\d]+',
                                    soup2.find("div" , class_="price-box price-final_price").find("span" , class_="price-wrapper").text)
                price = price1[0].replace(",","")
            except ValueError:
                price1 = re.findall(r'[\d]+',
                                    soup2.find("div" , class_="price-box price-final_price").find("span" , class_="price-wrapper").text)
                price = price1[0].replace(",","")
        except ValueError:
            price1 = re.findall(r'[\d]+',soup2.find("div" , class_="price-box price-final_price").text)
            price = price1[0].replace(",","")
        except:
            continue
        csv_writer.writerow(
            [name,Model, price, Avail, SKU[0], Outerunitdimension, Innerdimension, Manufacturer, productlink, sitename])

    file.close()
    main_data_frame = pd.read_csv("blackbox.csv")
    writer = pd.ExcelWriter(r'blackbox_excel_data.xlsx', engine='xlsxwriter')
    main_data_frame.to_excel(writer, index=False)
    writer.close()
#blackbox_scraping("https://blackbox.com.sa/ar/air-conditioners-accessories/air-conditioner/split.html")