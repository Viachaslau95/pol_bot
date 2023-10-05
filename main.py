# import random
# import threading
# import time
# import telebot
# from datetime import datetime
#
# from django.core.management import BaseCommand
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# chrome_options = Options()
#
# driver = webdriver.Chrome(options=chrome_options)
#
# driver.get("https://www.instagram.com/accounts/login/")
# time.sleep(5)
#
# driver.find_element(By.NAME, "username").send_keys('it6891094@gmail.com')
#
# driver.find_element(By.NAME, "password").send_keys('gjrfqae30')
# time.sleep(10)
# driver.find_element(By.XPATH, '//img[@alt="Фото профиля it6891094"]').click()
# followers = driver.find_elements(
#     By.CSS_SELECTOR,
#     'li.x6s0dn4.x78zum5.xvs91rp.xl56j7k.x2b8uid.x1ltjmfc.x2pgyrj.x4tmyev'
# )[1].text.split('\n')[0]
#
#
# time.sleep(120)

