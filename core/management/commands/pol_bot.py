import threading
import time
from datetime import datetime
from random import choice

from django.core.management import BaseCommand
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import LOGIN_URL
from core.models import Client, City

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)


# HOSTNAME = '37.17.38.196'
# PORT = '53281'
#
#
# def create_driver_with_proxy():
#     chrome_options.add_argument(f'--proxy-server=http://{HOSTNAME}:{PORT}')
#     driver = webdriver.Chrome(options=chrome_options)
#     return driver

# proxies = [
# "194.158.203.14:80",
# ]

# for proxy in proxies:
#     prox = Proxy()
#     prox.proxy_type = ProxyType.MANUAL
#     prox.http_proxy = proxy
#     prox.ssl_proxy = proxy
#     chrome_options.add_argument('--proxy-server=http://' + proxy)


class Command(BaseCommand):
    should_break = True

    def handle(self, *args, **options):
        num_users = Client.objects.filter(is_active=True).count()
        drivers = [webdriver.Chrome(options=chrome_options) for _ in range(num_users)]
        users_from_db = Client.objects.filter(is_active=True)
        threads = []

        for user_id, driver in enumerate(drivers):
            client = users_from_db[user_id % len(users_from_db)]
            thread = threading.Thread(target=self.login_and_city,
                                      args=(driver, user_id, client))
            threads.append(thread)
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
            # wait 30 min
            WebDriverWait(driver, 1800).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.fs-24.fs-sm-46.mb-25"))
            )
            time.sleep(3)

            while self.should_break:
                cities = City.objects.filter(clients=client)
                if cities.count() == 1:
                    element = driver.find_element(By.ID, "mat-select-0")
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(3)
                    for city in cities:
                        if city.title == "Center-Baranovichi":
                            driver.find_element(By.ID, "mat-option-1").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-0").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Brest":
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(3)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-1").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Gomel":
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(3)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(5)
                            self.second_city_group(driver, client, city)

                        if city.title == "Center-Grodno":
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(3)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Lida":
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-4").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Minsk":
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

                        if city.title == "Center-Mogilev":
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(5)
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-6").click()
                            time.sleep(3)
                            self.second_city_group(driver, client, city)

                        if city.title == "Center-Pinsk":
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
                        if city.title == "Center-Baranovichi":
                            driver.find_element(By.ID, "mat-option-0").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Brest":
                            driver.find_element(By.ID, "mat-option-1").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Gomel":
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(5)
                            self.second_city_group(driver, client, city)

                        if city.title == "Center-Grodno":
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(5)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Lida":
                            driver.find_element(By.ID, "mat-option-4").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                        if city.title == "Center-Minsk":
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(3)
                            if client.visa_sub_category == 'Postal D-visa':
                                self.first_city_group(driver, client, city)
                            else:
                                self.second_city_group(driver, client, city)

                        if city.title == "Center-Mogilev":
                            driver.find_element(By.ID, "mat-option-6").click()
                            time.sleep(3)
                            self.second_city_group(driver, client, city)

                        if city.title == "Center-Pinsk":
                            driver.find_element(By.ID, "mat-option-7").click()
                            time.sleep(3)
                            self.first_city_group(driver, client, city)

                # else:
                #     for city in range(8):
                #         element = driver.find_element(By.ID, "mat-select-0")
                #         driver.execute_script("arguments[0].click();", element)
                #         time.sleep(3)
                #         try:
                #             driver.find_element(By.ID, f"mat-option-{city}").click()
                #             time.sleep(5)
                #
                #             driver.find_element(By.ID, "mat-select-2").click()
                #             time.sleep(5)
                #
                #             national_visa_element = driver.find_element(By.XPATH, f"//span[text()=' {NATIONAL} ']")
                #             national_visa_element.click()
                #             time.sleep(3)
                #
                #             driver.find_element(By.ID, "mat-select-4").click()
                #             time.sleep(3)
                #
                #             driver.find_element(By.XPATH, f"//span[text()=' {OTHER} ']").click()
                #             time.sleep(3)
                #
                #             date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                #                                                       'input[formcontrolname="dateOfBirth"].form-control')
                #             date_of_birth_input.clear()
                #             date_of_birth_input.send_keys("23/10/1992")
                #             time.sleep(3)
                #
                #             driver.find_element(By.ID, "mat-select-value-7").click()
                #             time.sleep(3)
                #
                #             driver.find_element(By.XPATH, "//span[text()=' BELARUS ']").click()
                #             time.sleep(3)
                #
                #             try:
                #                 continue_button = driver.find_element(By.XPATH,
                #                                                       "//button[contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-raised-button')]")
                #                 time.sleep(3)
                #                 if "mat-button-disabled" in continue_button.get_attribute("class"):
                #                     print("The button is disabled. Continuing the loop.")
                #                     time.sleep(30)
                #                 else:
                #                     continue_button.click()
                #                     print("Button has been clicked")
                #                     self.your_detail(driver, client)
                #             except Exception:
                #                 print('Error continue')
                #
                #         except Exception as e:
                #             print(e)

        except Exception as e:
            print(f"User {user_id} error: {e}")

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

                self.date_of_birth_and_nationality(driver, client)
            else:
                self.schengen_visa_c(driver, client, city)
        except Exception as e:
            print(e)

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
                self.date_of_birth_and_nationality(driver, client)
            else:
                self.schengen_visa_c(driver, client, city)
        except Exception as e:
            print(e)

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

        elif city.title == "Center-Grodno":
            driver.find_element(By.ID, "mat-select-4").click()
            time.sleep(3)
            if client.visa_sub_category == "Other C visa":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' Other C visa ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "USA Embassy, KP exam/odbior C-Visa":
                driver.find_element(
                    By.XPATH,
                    "//mat-option[contains(@class, 'mat-option') and contains(., ' USA Embassy, KP exam/odbior C-Visa ')]"
                ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
        elif city.title == "Center-Lida":
            driver.find_element(By.ID, "mat-select-4").click()
            time.sleep(3)
            if client.visa_sub_category == "Other C visa":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' Other C visa ')]"
                                    ).click()
                time.sleep(3)
                self.date_of_birth_and_nationality(driver, client)
            elif client.visa_sub_category == "Tourism C-visa":
                driver.find_element(By.XPATH,
                                    "//mat-option[contains(@class, 'mat-option') and contains(., ' Tourism C-visa ')]"
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
                time.sleep(30)
            else:
                continue_button.click()
                print("Button has been clicked")
                self.should_break = False
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
            self.should_break = False
            print(Exception)

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
        try:
            wait = WebDriverWait(driver, 3600)
            button_locator = (By.XPATH, "//button[contains(., 'Add another applicant')]")
            wait.until(EC.presence_of_element_located(button_locator))
            print("Кнопка 'Add another applicant' появилась")

            self.find_slot(driver)
        except Exception as e:
            print("Произошла ошибка:", e)

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
        time.sleep(30)

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

            self.find_slot(driver)
        except Exception as e:
            print("Произошла ошибка:", e)

    def find_slot(self, driver):
        print("in find_slot")
        # while True:
        #     try:
        #         continue_button = driver.find_element(By.XPATH, "//button[contains(., 'Continue')]")
        #         time.sleep(5)
        #         continue_button.click()
        #
        #     except TimeoutException:
        #         print("Кнопка 'Continue' не появилась за 60 минут")
        #
        #     WebDriverWait(driver, 3600).until(
        #         EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Book an Appointment')]")))
        #     try:
        #         table = driver.find_element(By.CLASS_NAME, "fc-scrollgrid-sync-table")
        #         td_elements = table.find_elements(By.TAG_NAME, "td")
        #         count_page = 0
        #         desired_element_xpath = "//td[@class='fc-daygrid-day fc-day fc-day-fri fc-day-future date-availiable']"
        #         while count_page < 2:
        #             for td_element in td_elements:
        #                 if td_element.get_attribute("outerHTML") == driver.find_element(
        #                         By.XPATH, desired_element_xpath).get_attribute("outerHTML"):
        #                     time.sleep(2)
        #                     td_element.click()
        #                     time.sleep(3)
        #
        #                     try:
        #                         WebDriverWait(driver, 60).until(
        #                             EC.presence_of_element_located(
        #                                 (By.XPATH, "//h2[@class='fs-18 fs-sm-24 mt-40 mb-20 ng-star-inserted']")
        #                             )
        #                         )
        #                         time_element = driver.find_element(By.XPATH,
        #                                                            "//tr[@class='hidden-item ng-star-inserted']")
        #                         time_element.click()
        #                         time.sleep(5)
        #
        #                         driver.find_element(By.XPATH,
        #                                             "//button[contains(@class, 'mat-raised-button') and contains(.//span, 'Continue')]").click()
        #
        #                     except Exception as e:
        #                         print(e)
        #
        #
        #             driver.find_element(By.CLASS_NAME, "fc-next-button").click()
        #             count_page += 1
        #
        #         go_back_button = driver.find_element(By.XPATH,
        #                                              "//button[contains(@class, 'mat-stroked-button') and contains(.//span, 'Go Back')]")
        #         go_back_button.click()
        #         # ..........
        #         # driver.find_element(By.CLASS_NAME, "fc-prev-button").click()
        #     #
        #     except TimeoutException:
        #         print("Элемент <h1> с текстом 'Book an Appointment' не появился за 60 минут")
