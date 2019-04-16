from selenium import webdriver
import datetime
import sqlite3

start_time = datetime.datetime.now()
print(start_time)

start_url = [
    'https://www.bestbuy.com/site/unlocked-mobile-phones/all-unlocked-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005&qp=brand_facet%3DBrand~Motorola',
    'https://www.bestbuy.com/site/unlocked-mobile-phones/all-unlocked-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005&qp=brand_facet%3DBrand~Sony',
    'https://www.bestbuy.com/site/unlocked-mobile-phones/all-unlocked-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005&qp=brand_facet%3DBrand~Samsung',
    'https://www.bestbuy.com/site/unlocked-mobile-phones/all-unlocked-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005&qp=brand_facet%3DBrand~Nokia'
]
#driver = webdriver.Firefox()
#driver.get('https://www.bestbuy.com/site/unlocked-mobile-phones/all-unlocked-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005&qp=brand_facet%3DBrand~Motorola')
#driver.get('https://www.bestbuy.com/site/unlocked-mobile-phones/all-unlocked-cell-phones/pcmcat311200050005.c?id=pcmcat311200050005&qp=brand_facet%3DBrand~Sony')



def get_phone_url_list(url):
    phone_url_list = []
    driver = webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_class_name('us-link').click()

    try:
        driver.find_element_by_class_name('us-link').click()
        #for phone_name in driver.find_elements_by_class_name('sku-header'):
            #print(phone_name.text)
        for i in driver.find_elements_by_xpath('//h4/a[@href]'):
            phone_url_list.append(i.get_attribute('href'))
        return phone_url_list
    finally:
        driver.close() # close the driver

def get_phone_config(url):
    driver = webdriver.Firefox()
    #driver.get('https://www.bestbuy.com/site/sony-xperia-xz2-with-64gb-memory-cell-phone-unlocked-liquid-black/6219454.p?skuId=6219454')
    driver.get(url)
    driver.find_element_by_class_name('us-link').click()
    driver.find_element_by_class_name('us-link').click()
    #print(driver.page_source)
    #result = driver.page_source
    print(url)
    phone_name = driver.find_elements_by_xpath('//h1')[0].text
    print(phone_name)
    phone_price = driver.find_elements_by_xpath('//div[@class="priceView-hero-price priceView-customer-price"]/span')[0].text
    print(phone_price)
    img = driver.find_elements_by_xpath('//div[@class="primary-container"]/button/img[@src]')[0]
    phone_img = img.get_attribute('src')
    print(phone_img)

    #phone_conf = driver.find_element_by_class_name('row-value col-xs-6 body-copy-lg v-fw-regular')
    #print(phone_conf)

    print('+++++++++++++++')

    driver.close()
    return (str(phone_img),str(phone_name),str(phone_price))

def main():
    conn = sqlite3.connect('app.sqlite')
    c = conn.cursor()
    num = 1

    for i in ['bestbuy_sony','bestbuy_samsung','bestbuy_nokia']:
        print('+++++++++下载'+i+'+++++++++')
        c.execute('drop table %s' % i)
        c.execute('create table %s (img varchar(1000),name varchar(1000),price varchar(1000))'%i)
        for j in get_phone_url_list(start_url[num]):
            c.execute("insert into %s values (?,?,?)" %i,get_phone_config(j))
            conn.commit()

        num = num + 1

    conn.commit()
    conn.close()


''' 
#get_phone_config()
for url in start_url:
    #print(url)
    for phone_url in get_phone_url_list(url):
        print(phone_url)
        get_phone_config(phone_url)
        #break
'''
if __name__ =='__main__':
    main()
    end_time = datetime.datetime.now()
    print(end_time-start_time)
