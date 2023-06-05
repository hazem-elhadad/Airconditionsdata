from info import *
def xcite_scraping(url):
    chrome_options = Options()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    page=1
    linkat=[]
    counter=0
    while True:
        try:
            new_url=url+f"?page={page}"
            driver.get(new_url)
            sleep(10)
            linkslist=driver.find_element(By.XPATH,'/html/body/div[1]/main/div/div/div[3]').find_element(By.XPATH,'./ul').find_elements(By.XPATH,'./li')
            for ele in linkslist:
                href=ele.find_element(By.TAG_NAME,'a').get_attribute('href')
                linkat.append(href)
            if len(linkslist)==0:
                print("no next page")
                break
            page+=1
        except Exception as e :
            print("check for mistakes")
            break
    file=open('xcite.csv','w',encoding='utf-8',newline='')
    csv_writer=csv.writer(file)
    csv_writer.writerow(['اسم المنتج' ,'الموديل', 'السعر' ,'التوفر','SKU', 'الأبعاد الخارجية' ,'الأبعاد الداخلية','بلد الصنع','لينك المنتج','اسم الموقع'])
    for ahref in linkat:
        elementlink=ahref
        name = 'لا يوجد'
        Model="موجود بالاسم"
        price = 'لا يوجد'
        SKU = 'لا يوجد'
        Innerdimension = 'لا يوجد'
        Outerunitdimension = "لا يوجد"
        Avail = 'لا يوجد'
        Manufacturer = "لا يوجد"
        sitename="Xcite"
        driver.get(ahref)
        try:
            name = driver.find_element(By.XPATH,
                                   '//h1[@class="font-body rtl:font-rtl typography-default mb-5 sm:typography-h1 sm:mb-10"]').text
        except:pass
        try:
            Model =re.findall(r'\((.+?)\)' , name)[0].strip()
        except:
            try:
                Model = re.findall(r'(?<=-).*' , name)[0].strip()
            except:pass
        try:
            try:
                price1=re.findall(r'[\d]+[.,\d]+',driver.find_element(By.XPATH , '//h3[@class="mb-10"]').find_element(By.XPATH,'./div/span[2]').text)
                price = price1[0].replace(",","")
            except ValueError:
                price1 = re.findall(r'[\d]+',driver.find_element(By.XPATH, '//h3[@class="mb-10"]').find_element(By.XPATH,'./div/span[2]').text)
                price = price1[0].replace(",","")
        except ValueError:
            price1 = re.findall(r'[\d]+', driver.find_element(By.XPATH, '//h3[@class="mb-10"]').text)
            price = price1[0].replace(",","")
        except:continue
        try:
            SKU =re.findall(r'\d+',driver.find_element(By.XPATH , '//div[@class="flex items-center justify-start mb-2 sm:justify-start gap-x-5 sm:gap-x-10"]').find_element(By.XPATH,'./span').text)
        except:pass

        try:
            Avail1 =driver.find_element(By.XPATH , '//div[@class="flex items-center justify-start mb-2 sm:justify-start gap-x-5 sm:gap-x-10"]').find_element(By.XPATH,'./div').text
            if Avail1 =="In Stock":
                Avail="نعم"
        except:pass
        csv_writer.writerow(
            [name,Model, price, Avail, SKU[0], Outerunitdimension, Innerdimension, Manufacturer, elementlink,sitename])
        print(f"Finishing product Num: {counter}")
        counter += 1
    file.close()
    main_data_frame = pd.read_csv("xcite.csv")
    writer = pd.ExcelWriter(r'xcite_excel_data.xlsx', engine='xlsxwriter')
    main_data_frame.to_excel(writer, index=False)
    writer.close()


# xcite_scraping("https://www.xcite.com.sa/split-ac/c")

