import random
import threading
import time
import telebot
from datetime import datetime

from django.core.management import BaseCommand
import undetected_chromedriver as uc
# from undetected_chromedriver import ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import LOGIN_URL
from core.models import Client, City
from config.settings.local import tg_bot_token, chat_id,\
    CITY_1, CITY_2, CITY_3, CITY_4, CITY_5, CITY_6, CITY_7, CITY_8


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
]


chrome_options = Options()
# chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")

#
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')


bot = telebot.TeleBot(tg_bot_token)

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_states = {}

    def handle(self, *args, **options):
        num_users = Client.objects.filter(is_active=True).count()
        drivers = [webdriver.Chrome(options=chrome_options) for _ in range(num_users)]
        # drivers = [uc.Chrome(options=chrome_options) for _ in range(num_users)]
        users_from_db = Client.objects.filter(is_active=True)
        threads = []

        for user_id, driver in enumerate(drivers):
            client = users_from_db[user_id % len(users_from_db)]
            thread = threading.Thread(target=self.login_and_city,
                                      args=(driver, user_id, client))
            threads.append(thread)
            self.thread_states[thread] = "run"
            thread.start()

        for thread in threads:
            thread.join()

    def login_and_city(self, driver, user_id, client):
        try:
            while len(driver.window_handles) <= user_id:
                driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[user_id])

            # login
            driver.get(LOGIN_URL)
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.ID, "mat-input-0"))
            )
            driver.find_element(By.ID, "mat-input-0").send_keys(client.reg_email)
            time.sleep(2)
            driver.find_element(By.ID, "mat-input-1").send_keys(client.reg_password)
            time.sleep(2)
            print(f'{client.reg_email} - waiting for captcha solution')
            bot.send_message(chat_id=chat_id, text=f'{client.reg_email} - waiting for captcha solution')
            # wait 30 min
            WebDriverWait(driver, 1800).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.fs-24.fs-sm-46.mb-25"))
            )
            time.sleep(3)

            while self.thread_states[threading.current_thread()] != "stop":
                cities = City.objects.filter(clients=client)
                # try:
                #     warning_form = driver.find_element(By.CLASS_NAME, "mat-modal-delete-document")
                #
                #     if warning_form:
                #         print('xxxx')
                #         warning_form.find_element(By.XPATH, "//div[@class='col-12 col-sm']/button[@mat-stroked-button='']").click()
                #         time.sleep(20)
                #         try:
                #             driver.find_element(By.ID, "mat-input-0").send_keys(client.reg_email)
                #             time.sleep(2)
                #             driver.find_element(By.ID, "mat-input-1").send_keys(client.reg_password)
                #             time.sleep(2)
                #             print(f'{client.reg_email} - waiting for captcha solution')
                #             bot.send_message(chat_id=chat_id, text=f'{client.reg_email} - waiting for captcha solution')
                #             # wait 30 min
                #             WebDriverWait(driver, 1800).until(
                #                 EC.presence_of_element_located((By.CSS_SELECTOR, "h1.fs-24.fs-sm-46.mb-25"))
                #             )
                #             time.sleep(3)
                #         except Exception:
                #             print('first warning page')
                # except Exception:
                #     print('not warning_form')

                if cities.count() == 1:
                    element = driver.find_element(By.ID, "mat-select-0")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(3)
                    for city in cities:
                        if city.title == CITY_1:
                            driver.find_element(By.ID, "mat-option-1").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-0").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_2:
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(3)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-1").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_3:
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(3)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(5)
                            self.second_city_group(driver, client, city)

                        if city.title == CITY_4:
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(3)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_5:
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-4").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_6:
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(3)
                            if client.visa_sub_category == 'Postal D-visa':
                                self.first_city_group(driver, client, city)
                            else:
                                self.second_city_group(driver, client, city)

                        if city.title == CITY_7:
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-6").click()
                            time.sleep(3)
                            self.second_city_group(driver, client, city)

                        if city.title == CITY_8:
                            driver.find_element(By.ID, "mat-option-4").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-7").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                else:
                    for city in cities:
                        element = driver.find_element(By.ID, "mat-select-0")
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(3)
                        if city.title == CITY_1:
                            driver.find_element(By.ID, "mat-option-0").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_2:
                            driver.find_element(By.ID, "mat-option-1").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_3:
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(5)
                            self.second_city_group(driver, client, city)

                        if city.title == CITY_4:
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_5:
                            driver.find_element(By.ID, "mat-option-4").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == CITY_6:
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(3)
                            if client.visa_sub_category == 'Postal D-visa':
                                self.first_city_group(driver, client, city)
                            else:
                                self.second_city_group(driver, client, city)

                        if city.title == CITY_7:
                            driver.find_element(By.ID, "mat-option-6").click()
                            time.sleep(3)
                            self.second_city_group(driver, client, city)

                        if city.title == CITY_8:
                            driver.find_element(By.ID, "mat-option-7").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)


        except Exception as e:
            print(f"User {client.reg_email} error: {e}")
            bot.send_message(
                chat_id=chat_id,
                text=f'Клиент {client.lastname} | +375-{client.contact_number} : завершил выполнение в боте, без записи!'
            )

    def first_city_group(self, driver, client, city):
        try:
            driver.find_element(By.ID, "mat-select-2").click()
            time.sleep(5)

            if client.visa_type == "National Visa D":
                driver.find_element(By.XPATH,
                                    "//span[contains(@class, 'mat-option-text') and text()=' National Visa D ']").click()
                time.sleep(3)
                driver.find_element(By.ID, "mat-select-4").click()
                time.sleep(3)
                if client.visa_sub_category == 'Driver D-visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Driver D-visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Karta Polaka D-visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Karta Polaka D-visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Other D-visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Other D-visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Postal D-visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Postal D-visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Work D-visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Work D-visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Natsionalnaya Viza':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Natsionalnaya Viza ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Studencheskaya Viza':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Studencheskaya Viza ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'PRACA':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' PRACA ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Krajowa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Krajowa ']"
                    ).click()
                self.date_of_birth_and_nationality(driver, client)
            else:
                self.schengen_visa_c(driver, client, city)
        except Exception as e:
            print("in first city group", e)

    def second_city_group(self, driver, client, city):
        try:
            driver.find_element(By.ID, "mat-select-2").click()
            time.sleep(5)

            if client.visa_type == "National Visa D":
                driver.find_element(By.XPATH,
                                    "//span[contains(@class, 'mat-option-text') and text()=' National Visa D ']").click()
                time.sleep(3)
                driver.find_element(By.ID, "mat-select-4").click()
                time.sleep(3)
                if client.visa_sub_category == "D - Inne" or client.visa_sub_category == "D - National":
                    try:
                        driver.find_element(
                            By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Inne ']"
                        ).click()
                        time.sleep(2)
                    except Exception as ex:
                        print(f"{ex}\n 'D-Inne' not found")
                        driver.find_element(
                            By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - National ']"
                        ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Nacional':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Nacional ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Natsionalnaya Viza':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Natsionalnaya Viza ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - National Visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - National Visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Stydent':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Stydent ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Studenci' or client.visa_sub_category == 'D - Student':
                    try:
                        driver.find_element(
                            By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Studenci ']"
                        ).click()
                        time.sleep(2)
                    except Exception as ex:
                        print(f"{ex}\n 'D - Studenci' not found")
                        driver.find_element(
                            By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Student ']"
                        ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Student Visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Student Visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Studencheskaya Viza':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Studencheskaya Viza ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Uchenik':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Uchenik ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Uczniowie' or client.visa_sub_category == 'D - Uczen':
                    try:
                        driver.find_element(
                            By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Uczniowie ']"
                        ).click()
                        time.sleep(2)
                    except Exception as ex:
                        print(f"{ex}\n 'D - Uczniowie' not found")
                        driver.find_element(
                            By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Uczen ']"
                        ).click()
                        time.sleep(2)
                elif client.visa_sub_category == 'D - Uczen Visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Uczen Visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'PBH D-visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' PBH D-visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - PBH':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - PBH ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - PBH Visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - PBH Visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'PRACA':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' PRACA ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Krajowa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' Krajowa ']"
                    ).click()
                    time.sleep(2)
                self.date_of_birth_and_nationality(driver, client)
            else:
                self.schengen_visa_c(driver, client, city)
        except Exception as e:
            print('in second city group', e)

    def schengen_visa_c(self, driver, client, city):
        driver.find_element(By.XPATH,
                            "//span[contains(@class, 'mat-option-text') and text()=' Schengen Visa C ']").click()
        time.sleep(3)

        if city.title == "Center-Minsk":
            driver.find_element(By.ID, "mat-select-4").click()
            time.sleep(3)
            if client.visa_sub_category == "C - Biznes":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' C - Biznes ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "C - Business Visa":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' C - Business Visa ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "C - Culture Visa":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' C - Culture Visa ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "C - Kultura":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' C - Kultura ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "C - Odwiedziny":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' C - Odwiedziny ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "C - Schengen":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' C - Schengen ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "C - Visit Visa":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' C - Visit Visa ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "Schengenskaya - Wojewodskoe priglashenie":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' Schengenskaya - Wojewodskoe priglashenie ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "Schengenskaya Viza":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' Schengenskaya Viza ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)

        # elif city.title == "Center-Grodno":
        #     driver.find_element(By.ID, "mat-select-4").click()
        #     time.sleep(3)
        #     if client.visa_sub_category == "Other C visa":
        #         driver.find_element(By.XPATH,
        #                             "//mat-option[contains(@class, 'mat-option') and contains(., ' Other C visa ')]"
        #                             ).click()
        #         time.sleep(3)
        #         self.date_of_birth_and_nationality(driver, client)
        #     elif client.visa_sub_category == "USA Embassy, KP exam/odbior C-Visa":
        #         driver.find_element(
        #             By.XPATH,
        #             "//mat-option[contains(@class, 'mat-option') and contains(., ' USA Embassy, KP exam/odbior C-Visa ')]"
        #         ).click()
        #         time.sleep(3)
        #         self.date_of_birth_and_nationality(driver, client)
        # elif city.title == "Center-Lida":
        #     driver.find_element(By.ID, "mat-select-4").click()
        #     time.sleep(3)
        #     if client.visa_sub_category == "Other C visa":
        #         driver.find_element(By.XPATH,
        #                             "//mat-option[contains(@class, 'mat-option') and contains(., ' Other C visa ')]"
        #                             ).click()
        #         time.sleep(3)
        #         self.date_of_birth_and_nationality(driver, client)
        #     elif client.visa_sub_category == "Tourism C-visa":
        #         driver.find_element(By.XPATH,
        #                             "//mat-option[contains(@class, 'mat-option') and contains(., ' Tourism C-visa ')]"
        #                             ).click()
        #         time.sleep(3)
        #         self.date_of_birth_and_nationality(driver, client)
        elif city.title == "Center-Gomel" or city.title == "Center-Mogilev":
            driver.find_element(By.ID, "mat-select-4").click()
            time.sleep(3)
            if client.visa_sub_category == "Schengenskaya - Wojewodskoe priglashenie":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' Schengenskaya - Wojewodskoe priglashenie ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "Schengenskaya Viza":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' Schengenskaya Viza ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
        else:
            time.sleep(3)
            self.date_of_birth_and_nationality(driver, client)

    def date_of_birth_and_nationality(self, driver, client):
        date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                  'input[formcontrolname="dateOfBirth"].form-control')
        date_of_birth_input.clear()
        date_of_birth_input.send_keys(client.date_of_birth)
        time.sleep(15)

        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located(
                (By.ID, "mat-select-6")
            )
        ).click()
        time.sleep(3)

        driver.find_element(By.XPATH, "//span[text()=' BELARUS ']").click()
        time.sleep(3)
        try:
            continue_button = driver.find_element(
                By.XPATH, "//button[contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-raised-button')]"
            )
            time.sleep(3)
            if "mat-button-disabled" in continue_button.get_attribute("class"):
                print("The button is disabled. Continuing the loop.")
                random_time_sleep = random.choice([300, 360, 420])
                time.sleep(random_time_sleep)
            else:
                continue_button.click()
                print("Button has been clicked")
                self.thread_states[threading.current_thread()] = "stop"
                current_date = datetime.now()
                birth_date = datetime.strptime(client.date_of_birth, "%d/%m/%Y")
                age = current_date.year - birth_date.year
                if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
                    age -= 1
                if age < 18:
                    self.your_detail_without_msi(driver,client)
                elif age > 58 and client.gender == "Female":
                    self.your_detail_without_msi(driver, client)
                elif age > 63 and client.gender == "Male":
                    self.your_detail_without_msi(driver, client)
                else:
                    self.your_detail(driver, client)
        except Exception:
            bot.send_message(
                chat_id=chat_id,
                text=f'Клиент {client.lastname} | +375-{client.contact_number} : Не завершил регистрацию '
                     f'Завершите в ручную чтобы не потерять СЛОТ!'
            )
            self.thread_states[threading.current_thread()] = "stop"
            print("in date_of_birth_and_nationality", Exception)

    def your_detail(self, driver, client):
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//h5[@class='mb-20 ng-star-inserted']"))
        )

        driver.find_element(By.ID, "mat-input-2").send_keys(client.national_id)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-4").send_keys(client.firstname)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-5").send_keys(client.lastname)
        time.sleep(3)

        driver.find_element(By.ID, "mat-select-8").click()
        time.sleep(2)
        if client.gender == 'Female':
            gender_option = " Female "
        elif client.gender == 'Male':
            gender_option = " Male "
        else:
            gender_option = " Others / Transgender "

        driver.find_element(By.XPATH,
                            f"//span[contains(@class, 'mat-option-text') and text()='{gender_option}']").click()
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-6").send_keys(client.passport_number)
        time.sleep(3)

        driver.find_element(By.ID, "passportExpirtyDate").send_keys(client.passport_expire_date)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-7").send_keys(client.code_country)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-8").send_keys(client.contact_number)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-9").send_keys(client.admin_email)
        time.sleep(3)
        bot.send_message(
            chat_id=chat_id,
            text=f'Клиент {client.lastname} | +375-{client.contact_number} : Ожидает MSI'
        )
        try:
            wait = WebDriverWait(driver, 3600)
            button_locator = (By.XPATH, "//button[contains(., 'Add another applicant')]")
            wait.until(EC.presence_of_element_located(button_locator))
            print("Кнопка 'Add another applicant' появилась")
            print(f"{client.reg_email} - trying to enter in find slot! ")

            self.find_slot(driver, client)
        except Exception as e:
            print(f"Error user {client.reg_email}:", e)

        # driver.find_element(By.XPATH, "//button[contains(@class, 'mat-stroked-button') and text()=' Save ']").click()

    def your_detail_without_msi(self, driver, client):
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, "mat-input-2"))
        )
        driver.find_element(By.ID, "mat-input-2").send_keys(client.firstname)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-3").send_keys(client.lastname)
        time.sleep(3)

        driver.find_element(By.ID, "mat-select-8").click()
        time.sleep(2)
        if client.gender == 'Female':
            gender_option = " Female "
        elif client.gender == 'Male':
            gender_option = " Male "
        else:
            gender_option = " Others / Transgender "

        driver.find_element(By.XPATH,
                            f"//span[contains(@class, 'mat-option-text') and text()='{gender_option}']").click()
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-4").send_keys(client.passport_number)
        time.sleep(3)

        driver.find_element(By.ID, "passportExpirtyDate").send_keys(client.passport_expire_date)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-5").send_keys(client.code_country)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-6").send_keys(client.contact_number)
        time.sleep(3)

        driver.find_element(By.ID, "mat-input-7").send_keys(client.admin_email)
        time.sleep(10)

        driver.find_element(By.XPATH, "//span[contains(text(), 'Save')]").click()
        time.sleep(3)

        bot.send_message(
            chat_id=chat_id,
            text=f'Клиент {client.lastname} | +375-{client.contact_number} : Ожидает OTP или нажатия на кнопку!'
        )


        # try:
        #     button_save = driver.find_element(By.XPATH, "//span[contains(text(), 'Save')]")
        #     button_save.click()
        #     time.sleep(30)
        #     wait = WebDriverWait(driver, 200)
        #     element = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Generate OTP']")))
        #
        #     self.some(driver)
        # except Exception:
        #     print("Error in 'your_detail_without_msi'!!! ")

        try:
            wait = WebDriverWait(driver, 3600)
            button_locator = (By.XPATH, "//button[contains(., 'Add another applicant')]")
            wait.until(EC.presence_of_element_located(button_locator))
            print("Кнопка 'Add another applicant' появилась")
            print(f"{client.reg_email} - trying to enter in find slot! ")
            self.find_slot(driver, client)
        except Exception as e:
            print(f"Error user {client.reg_email}:", e)

    def find_slot(self, driver, client):
        print("in find_slot")
        WebDriverWait(driver, 3600).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Book an Appointment')]"))
        )
        try:
            element = WebDriverWait(driver, 180).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[contains(text(), 'Available')]")
                )
            )

            if element:
                bot.send_message(
                    chat_id=chat_id,
                    text=f'Бот нашел свободные слоты для: {client.lastname} | +375-{client.contact_number}'
                )
                time.sleep(7)

                # slot day
                driver.find_element(
                    By.CSS_SELECTOR, "td.fc-day-future.date-availiable"
                ).click()
                time.sleep(2)

                try:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.table-responsive-lg table.table tbody"))
                    )

                    # slot time
                    driver.find_element(By.CSS_SELECTOR, "tr.hidden-item.ng-star-inserted").click()
                    time.sleep(2)

                    driver.find_element(By.XPATH, "//span[contains(text(), 'Continue')]").click()
                    time.sleep(3)

                    self.services_page(driver, client)

                except Exception as e:
                    print(f'{client.reg_email} ERROR in slot time! - {e}')

            elif not element:
                driver.find_element(By.CLASS_NAME, "fc-next-button").click()
                element_2_page = WebDriverWait(driver, 180).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Available')]")
                                                   )
                )
                if element_2_page:
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'Бот нашел свободные слоты для: {client.lastname} | +375-{client.contact_number}'
                    )
                    time.sleep(15)

                    # slot day
                    driver.find_element(
                        By.CSS_SELECTOR, "td.fc-day-future.date-availiable"
                    ).click()
                    time.sleep(2)

                    try:
                        WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, "div.table-responsive-lg table.table tbody")
                            )
                        )

                        # slot time
                        driver.find_element(By.CSS_SELECTOR, "tr.hidden-item.ng-star-inserted").click()
                        time.sleep(2)

                        driver.find_element(By.XPATH, "//span[contains(text(), 'Continue')]").click()
                        time.sleep(3)

                        self.services_page(driver, client)
                    except Exception as e:
                        print("Произошла ошибка:", str(e))
                else:
                    bot.send_message(
                        chat_id=chat_id,
                        text=f'Для Клиентa {client.lastname} | +375-{client.contact_number} - нет свободных слотов(Пустышка).'
                             f'Бот завершил работу для этого клиента'
                    )
                    driver.close()
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=f'Для Клиентa {client.lastname} | +375-{client.contact_number} - нет свободных слотов(Пустышка).'
                         f'Бот завершил работу для этого клиента'
                )
                driver.close()
        except Exception as e:
            print(f'{client.reg_email} ERROR in find slot! - {e}')
            bot.send_message(
                chat_id=chat_id,
                text=f'БОТ НЕ СМОГ ВЫБРАТЬ ДАТУ!!! ЗАВЕРШИТЕ ЗАПОЛНЕНИЕ ВРУЧНУЮ. Чтобы не потерять слот.')

    def services_page(self,driver, client):
        bot.send_message(
            chat_id=chat_id,
            text=f'Клиент {client.lastname} | +375-{client.contact_number} : находится на странице services!'
        )
        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[contains(@class, 'fs-24') and contains(text(), 'Services')]"))
        )
        time.sleep(5)
        driver.find_element(By.XPATH, "//span[contains(text(), 'Continue')]").click()
        time.sleep(3)

        self.review_page(driver, client)

    def review_page(self, driver, client):
        bot.send_message(
            chat_id=chat_id,
            text=f'Клиент {client.lastname} | +375-{client.contact_number} :находится на последней странице! Завершите регистрацию!'

        )

        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Review')]"))
        )
        time.sleep(2)
        try:
            driver.find_element(
                By.XPATH,
                "//div[@class='form-group mb-20 ng-star-inserted']//mat-checkbox[@id='mat-checkbox-1']"
            ).click()
            time.sleep(3)
            confirm_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Confirm')]")
            # confirm_button.click()

        except Exception:
            bot.send_message(
                chat_id=chat_id,
                text=f'БОТ НЕ СМОГ поставить галочку на последней странице!!!'
                     f' ЗАВЕРШИТЕ ЗАПОЛНЕНИЕ ВРУЧНУЮ. Чтобы не потерять слот.')




