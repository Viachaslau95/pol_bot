import threading
import time
from random import choice

from django.core.management import BaseCommand
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import LOGIN_URL, NATIONAL, OTHER, WORK
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

class Command(BaseCommand):
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
            if len(driver.window_handles) <= user_id:
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
            # wait 10 min
            WebDriverWait(driver, 600).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.fs-24.fs-sm-46.mb-25"))
            )
            time.sleep(3)
            while True:
                cities = City.objects.filter(clients=client)
                if cities:
                    for city in cities:
                        if city.title == "Center-Baranovichi":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-0").click()
                            time.sleep(5)
                            self.first_city_group(driver, client)

                        if city.title == "Center-Brest":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-1").click()
                            time.sleep(5)
                            self.first_city_group(driver, client)

                        if city.title == "Center-Gomel":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-2").click()
                            time.sleep(5)
                            self.second_city_group(driver, client)

                        if city.title == "Center-Grodno":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-3").click()
                            time.sleep(5)
                            self.first_city_group(driver, client)

                        if city.title == "Center-Lida":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-4").click()
                            time.sleep(5)
                            self.first_city_group(driver, client)

                        if city.title == "Center-Minsk":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-5").click()
                            time.sleep(5)
                            if client.visa_sub_category == 'Postal D-visa':
                                self.first_city_group(driver, client)
                            else:
                                self.second_city_group(driver, client)

                        if city.title == "Center-Mogilev":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-6").click()
                            time.sleep(5)
                            self.second_city_group(driver, client)

                        if city.title == "Center-Pinsk":
                            element = driver.find_element(By.ID, "mat-select-0")
                            driver.execute_script("arguments[0].click();", element)
                            time.sleep(3)
                            driver.find_element(By.ID, "mat-option-7").click()
                            time.sleep(5)
                            self.first_city_group(driver, client)

                else:
                    for city in range(8):
                        element = driver.find_element(By.ID, "mat-select-0")
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(3)
                        try:
                            driver.find_element(By.ID, f"mat-option-{city}").click()
                            time.sleep(5)

                            driver.find_element(By.ID, "mat-select-2").click()
                            time.sleep(5)

                            national_visa_element = driver.find_element(By.XPATH, f"//span[text()=' {NATIONAL} ']")
                            national_visa_element.click()
                            time.sleep(3)

                            driver.find_element(By.ID, "mat-select-4").click()
                            time.sleep(3)

                            driver.find_element(By.XPATH, f"//span[text()=' {OTHER} ']").click()
                            time.sleep(3)

                            date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                                      'input[formcontrolname="dateOfBirth"].form-control')
                            date_of_birth_input.clear()
                            date_of_birth_input.send_keys("23/10/1992")
                            time.sleep(3)

                            driver.find_element(By.ID, "mat-select-value-7").click()
                            time.sleep(3)

                            driver.find_element(By.XPATH, "//span[text()=' BELARUS ']").click()
                            time.sleep(3)

                            try:
                                continue_button = driver.find_element(By.XPATH,
                                                                      "//button[contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-raised-button')]")
                                time.sleep(3)
                                if "mat-button-disabled" in continue_button.get_attribute("class"):
                                    print("The button is disabled. Continuing the loop.")
                                else:
                                    continue_button.click()
                                    print("Button has been clicked")
                                    self.your_detail(driver, client)
                            except Exception:
                                print('Error continue')

                        except Exception as e:
                            print(e)

        except Exception as e:
            print(f"User {user_id} error: {e}")

    def first_city_group(self, driver, client):
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

                date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                          'input[formcontrolname="dateOfBirth"].form-control')
                date_of_birth_input.clear()
                date_of_birth_input.send_keys(client.date_of_birth)
                time.sleep(5)

                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.ID, "mat-select-6")
                    )
                ).click()
                time.sleep(3)

                driver.find_element(By.XPATH, "//span[text()=' BELARUS ']").click()
                time.sleep(3)
                try:
                    continue_button = driver.find_element(By.XPATH,
                                                          "//button[contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-raised-button')]")
                    time.sleep(3)
                    if "mat-button-disabled" in continue_button.get_attribute("class"):
                        print("The button is disabled. Continuing the loop.")
                        time.sleep(60)
                    else:
                        continue_button.click()
                        print("Button has been clicked")
                        self.your_detail(driver, client)
                except Exception:
                    print('Error continue')
            else:
                driver.find_element(By.XPATH,
                                    "//span[contains(@class, 'mat-option-text') and text()=' Schengen Visa C ']").click()
                time.sleep(3)
                date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                          'input[formcontrolname="dateOfBirth"].form-control')
                date_of_birth_input.clear()
                date_of_birth_input.send_keys(client.date_of_birth)
                time.sleep(3)
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.ID, "mat-select-6")
                    )
                ).click()
                time.sleep(3)

                driver.find_element(By.XPATH, "//span[text()=' BELARUS ']").click()
                time.sleep(3)

                try:
                    continue_button = driver.find_element(By.XPATH,
                                                          "//button[contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-raised-button')]")
                    time.sleep(3)
                    if "mat-button-disabled" in continue_button.get_attribute("class"):
                        print("The button is disabled. Continuing the loop.")
                    else:
                        continue_button.click()
                        print("Button has been clicked")
                        self.your_detail(driver, client)
                except Exception:
                    print('Error continue')

        except Exception as e:
            print(e)

    def second_city_group(self, driver, client):
        try:
            driver.find_element(By.ID, "mat-select-2").click()
            time.sleep(5)

            if client.visa_type == "National Visa D":
                driver.find_element(By.XPATH,
                                    "//span[contains(@class, 'mat-option-text') and text()=' National Visa D ']").click()
                time.sleep(3)
                driver.find_element(By.ID, "mat-select-4").click()
                time.sleep(3)
                if client.visa_sub_category == "D - National":
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - National ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - National Visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - National Visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Student':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Student ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Student Visa':
                    driver.find_element(
                        By.XPATH, "//span[contains(@class, 'mat-option-text') and text()=' D - Student Visa ']"
                    ).click()
                    time.sleep(2)
                elif client.visa_sub_category == 'D - Uczen':
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

                date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                          'input[formcontrolname="dateOfBirth"].form-control')
                date_of_birth_input.clear()
                date_of_birth_input.send_keys(client.date_of_birth)
                time.sleep(5)

                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.ID, "mat-select-6")
                    )
                ).click()
                time.sleep(3)

                driver.find_element(By.XPATH, "//span[text()=' BELARUS ']").click()
                time.sleep(3)
                try:
                    continue_button = driver.find_element(By.XPATH,
                                                          "//button[contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-raised-button')]")
                    time.sleep(3)
                    if "mat-button-disabled" in continue_button.get_attribute("class"):
                        print("The button is disabled. Continuing the loop.")
                        time.sleep(60)
                    else:
                        continue_button.click()
                        print("Button has been clicked")
                        self.your_detail(driver, client)
                except Exception:
                    print('Error continue')
            else:
                driver.find_element(By.XPATH,
                                    "//span[contains(@class, 'mat-option-text') and text()=' Schengen Visa C ']").click()
                time.sleep(3)
                date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                          'input[formcontrolname="dateOfBirth"].form-control')
                date_of_birth_input.clear()
                date_of_birth_input.send_keys(client.date_of_birth)
                time.sleep(3)
                WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located(
                        (By.ID, "mat-select-6")
                    )
                ).click()
                time.sleep(3)

                driver.find_element(By.XPATH, "//span[text()=' BELARUS ']").click()
                time.sleep(3)

                try:
                    continue_button = driver.find_element(By.XPATH,
                                                          "//button[contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-raised-button')]")
                    time.sleep(3)
                    if "mat-button-disabled" in continue_button.get_attribute("class"):
                        print("The button is disabled. Continuing the loop.")
                    else:
                        continue_button.click()
                        print("Button has been clicked")
                        self.your_detail(driver, client)
                except Exception:
                    print('Error continue')
        except Exception as e:
            print(e)

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

        # driver.find_element(By.XPATH, "//button[contains(@class, 'mat-stroked-button') and text()=' Save ']").click()
