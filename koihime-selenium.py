from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.options import Options
import time
from bottle import route, run, template, redirect, request
import schedule

@route("/")
def output():
    info = scraping()
    return template("index", title=info[0], element=info[1], date=info[2], image=info[3])

def scraping():
    options = Options()
    options.add_argument('--headless')
    CHROMEDRIVER = r'C:\Users\Akama\Desktop\Engineering\Python\chrome_driver\chromedriver.exe'
    chrome_service = fs.Service(executable_path=CHROMEDRIVER)
    driver = webdriver.Chrome(service=chrome_service, options=options)
    driver.get('http://baseson.nexton-net.jp/koihime-portal/')
    title = driver.find_element(By.CSS_SELECTOR, 'section#information > ul > li:first-child > a.link-motion.b-box > div.box01 > div.text.b-box > h4')
    element = driver.find_element(By.CSS_SELECTOR, 'section#information > ul > li:first-child > a.link-motion.b-box > div.box01 > div.text.b-box > p')
    date = driver.find_element(By.CSS_SELECTOR, 'section#information > ul > li:first-child > a.link-motion.b-box > div.box02.b-box > p:first-child')
    image = driver.find_element(By.CSS_SELECTOR, 'section#information > ul > li:first-child > a.link-motion.b-box > div.box01 > div.image > img')
    image_src = image.get_attribute('src')
    return title.text, element.text, date.text, image_src

if __name__ == "__main__":
    run(host="localhost", port=1055, debug=True, reloader=True)

schedule.every().wednesday.at("12:00").do(scraping)

while True:
    schedule.run_pending()
    time.sleep(1)