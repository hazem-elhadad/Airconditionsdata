from info import *

def swsg_scraping(url):
    options = uc.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = uc.Chrome()
    file = open('swsg.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    csv_writer.writerow(
        ['اسم المنتج','الموديل', 'السعر', 'التوفر', 'SKU', 'الأبعاد الخارجية', 'الأبعاد الداخلية', 'بلد الصنع', 'لينك المنتج','اسم الموقع'])
    linkat1 = []
    finallinks=[]
    page=1
    while True:
        try:
            new_url=url.split('=')[-2]+f"={page}"
            driver.get(new_url)
            sleep(15)
            links = driver.find_element(By.XPATH,'//div[@class="gallery-items-33P"]').find_elements(By.XPATH ,'//div[@class="home-products_grid_item-3F-"]')
            for ele1 in links:
                href=ele1.find_element(By.TAG_NAME ,'a').get_attribute('href')
                linkat1.append(href)

            if len(links) ==0:
                break
            page += 1
            finallinks=set(linkat1)
            if len(linkat1)>len(finallinks):
                break
            # if page ==2:break
            print("Going to next page")
        except Exception as e:
            print("check for mistakes!!")
            break
    print(len(finallinks))
    i =0
    for ele2 in finallinks:
        elementlink=ele2
        name = 'لا يوجد'
        Model='موجود بالاسم'
        price = 'لا يوجد'
        SKU = 'لا يوجد'
        Innerdimension = 'لا يوجد'
        Outerunitdimension = "لا يوجد"
        Avail = 'لا يوجد'
        Manufacturer = "لا يوجد"
        sitename="الشتاءوالصيف"
        try:
            Modellist = []
            ascilist=[]
            driver.get(ele2)
            sleep(3)
            try:
                Datatable = driver.find_element(By.XPATH,
                                                '//section[@class="undefined productFullDetail-shadow_section-2_e"]')
            except:
                pass
            try:
                name = Datatable.find_element(By.TAG_NAME, 'h1').text
            except:
                pass
            try:
                SKU = re.findall(r'\d+', Datatable.find_element(By.XPATH,
                                                                '//span[@class="productFullDetail-sku_details_val-Pff"]').text)
            except:
                pass
            try:
                Avail1 = Datatable.find_element(By.XPATH, '//span[@class="productFullDetail-stock_text-2eF ml-2"]').text
                if Avail1 == "متوفر الكمية":
                    Avail = "نعم"
            except:
                pass
            try:
                try:
                    price1 = re.findall(r'[\d]+[.,\d]+', Datatable.find_element(By.XPATH,
                                                                                '//p[@class="productFullDetail-productPrice-1Js"]').text)
                    price = price1[0].replace(",", "")
                except ValueError:
                    price1 = re.findall(r'[\d]+', Datatable.find_element(By.XPATH,
                                                                         '//p[@class="productFullDetail-productPrice-1Js"]').text)
                    price = price1[0].replace(",", "")
            except ValueError:
                price1 = re.findall(r'[\d]+', driver.find_element(By.XPATH,
                                                                  '//div[@class="productFullDetail-productpageprice-gEc"]').text)
                price = price1[0].replace(",", "")
            except:
                continue
            try:
                try:
                    detail_button = driver.find_element(By.XPATH, '//a[@id = "pills-home-tab"]')
                    detail_button.click()
                    sleep(4)
                except:pass
                try:
                    table=driver.find_element(By.XPATH,'//div[@id ="pills-tabContent"]').find_elements(By.TAG_NAME,'p')
                except:
                    table =driver.find_element(By.XPATH,'//div[@id ="pills-tabContent"]').find_elements(By.TAG_NAME,'span')
                for sec in table:
                    try:
                        if "موديل :" in sec.text or "الموديل:" in sec.text or "الموديل :" in sec.text:
                            Mode1 = sec.text
                            Model=re.findall(r":(.*)",Mode1)[0]

                    except:
                        try:
                            if "رقم الموديل:" in sec.find_element(By.TAG_NAME ,'strong').text:
                                Mode2 = sec.find_element(By.TAG_NAME ,'strong').text
                                Model =re.findall(r":(.*)",Mode2)[0]
                        except:pass
                    if "صيني" in sec.text or "الصناعة" in sec.text:
                        Manufacturer = "الصين"
            except:
                pass
            i += 1
            print(f"We are Now in link {i}")
            if Model == 'موجود بالاسم':
                Model2 = name.split(" ")
                Model=Model2[-1]
        except:continue
        csv_writer.writerow(
            [name,Model.strip(), price, Avail, SKU[0], Outerunitdimension, Innerdimension, Manufacturer, elementlink, sitename])

    file.close()
    main_data_frame = pd.read_csv("swsg.csv")
    writer = pd.ExcelWriter(r'swsg_excel_data.xlsx', engine='xlsxwriter')
    main_data_frame.to_excel(writer, index=False)
    writer.close()
swsg_scraping("https://swsg.co/ar/air-conditions.html?page=1")