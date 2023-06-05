from info import *

def alkhunaizan_scraping(url):
    options = uc.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = uc.Chrome()
    linkat=[]
    counter =0

    driver.get("https://alkhunaizan.sa/air-condition.html")
    i=0
    while True:
        try:
            sleep(1)
            ele1=driver.find_element(By.XPATH ,'/html/body/div[2]/main/div[3]/div[2]/div[1]/div[3]/div[2]/ol/li[134]')
            if ele1.get_attribute('class')=="item product product-item":
                break
        except:
            actions = ActionChains(driver)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            sleep(5)


    linkslist=driver.find_element(By.XPATH,'//ol[@class="products list items product-items flex-grid"]').find_elements(By.XPATH,'//li[@class="item product product-item"]')
    file=open('alkhunaizan.csv','w',encoding='utf-8',newline='')
    csv_writer=csv.writer(file)
    csv_writer.writerow(['اسم المنتج' ,'الموديل' , 'السعر' ,'التوفر','SKU', 'الأبعاد الخارجية' ,'الأبعاد الداخلية','بلد الصنع','لينك المنتج','اسم الموقع'])
    for ele in linkslist:
        i+=1
        print(f"we are in link {i}")
        href=ele.find_element(By.TAG_NAME,'a').get_attribute('href')
        linkat.append(href)
    for ele2 in linkat:
        name = 'لا يوجد'
        Model='موجود بالاسم'
        price = 'لا يوجد'
        SKU = 'لا يوجد'
        Innerdimension = 'لا يوجد'
        Outerunitdimension = "لا يوجد"
        Avail = 'لا يوجد'
        Manufacturer = "لا يوجد"
        driver.get(ele2)
        print(f"we got {ele2}")
        data=driver.find_element(By.XPATH,'//div[@class="product-right col-sm-12"]')
        name=data.find_element(By.XPATH , '//span[@itemprop="name"]').text
        try:
            Avail1=data.find_element(By.XPATH, '//div[@title="Availability"]').find_element(By.XPATH,'./span').text
            if Avail1 =="متوفر":
                Avail="نعم"
        except:pass
        SKU=re.findall(r'\d+',data.find_element(By.XPATH , '//div[@itemprop="sku"]').text)
        sitename="الخنيزان"
        try:
            try:
                price1=re.findall(r'[\d]+[.,\d]+',data.find_element(By.XPATH ,'//div[@class="price-box price-final_price"]').find_element(By.TAG_NAME,'span').text)
                price = price1[0].replace(",","")
            except ValueError:
                price1 = re.findall(r'[\d]+',data.find_element(By.XPATH ,'//div[@class="price-box price-final_price"]').find_element(By.TAG_NAME,'span').text)
                price = price1[0].replace(",","")
        except ValueError:
            price1 = re.findall(r'[\d]+', driver.find_element(By.XPATH, '//*[@id="product_addtocart_form"]/div/div[2]/div[2]/div[2]/div[2]').text)
            price = price1[0].replace(",","")
        except:continue
        try:
            Datatable=driver.find_element(By.XPATH,'//table[@id="product-attribute-specs-table"]/tbody').find_elements(By.TAG_NAME,'tr')
            for manu in Datatable:
                if manu.find_element(By.XPATH,'./th').text =="الصناعة":
                    Manufacturer= manu.find_element(By.XPATH,'./td').text
                if "موديل" in manu.find_element(By.XPATH,'./th').text:
                    Model= manu.find_element(By.XPATH,'./td').text
        except:pass
        print(Avail)
        csv_writer.writerow(
            [name,Model, price, Avail, SKU[0], Outerunitdimension, Innerdimension, Manufacturer, ele2, sitename])

    file.close()
    main_data_frame = pd.read_csv("alkhunaizan.csv")
    writer = pd.ExcelWriter(r'alkhunaizan_excel_data.xlsx', engine='xlsxwriter')
    main_data_frame.to_excel(writer, index=False)
    writer.close()


# alkhunaizan_scraping("https://alkhunaizan.sa/air-condition.html")