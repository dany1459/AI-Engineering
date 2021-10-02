import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

url = "https://app.eduflow.com/courses/de0a5ab8-2161-4deb-9ed4-cf6aef2433ca/flows/11984e7a-02ed-4128-a78f-b1a62d7d802b/activities/6b2b9749-001d-4a8e-b95e-129e71554cf8"
my_driver = "C:/Users/Igor/Documents/GitHub/AI-Exercises/Chapter 1/7. Web-scraping/chromedriver.exe"
driver = webdriver.Chrome(my_driver)
driver.get(url)

sleep(1)

user_box = driver.find_element_by_xpath('//*[@id="id_username"]')
user_box.send_keys("USERNAME HERE")

passw_box = driver.find_element_by_xpath('//*[@id="id_password"]')
passw_box.send_keys("PASSWORD HERE" + Keys.RETURN)

sleep(1)

play_video = driver.find_element_by_xpath('//*[@id="layout-section"]/div/div[1]/div[2]/div/figure')
play_video.click()

sleep(5)

pause_video = driver.find_element_by_xpath('//*[@id="layout-section"]/div/div[1]/div[2]/div/figure')
pause_video.click()
