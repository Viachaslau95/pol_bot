import threading
import time

from django.core.management import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import LOGIN_URL, NATIONAL, OTHER, WORK
from core.models import Client, City

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("detach", True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        num_users = Client.objects.filter(is_active=True).count()
        drivers = [webdriver.Chrome(options=chrome_options) for _ in range(num_users)]
        users_from_db = Client.objects.filter(is_active=True)
        threads = []

        for user_id, driver in enumerate(drivers):
            client = users_from_db[user_id % len(users_from_db)]
            # email = client.reg_email
            # password = client.reg_password
            thread = threading.Thread(target=self.login_and_first_page,
                                      args=(driver, user_id, client))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def login_and_first_page(self, driver, user_id, client):
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
                            self.baranovichi(driver, client)

                        if city.title == "Center-Brest":
                            self.brest(driver, client)

                        if city.title == "Center-Gomel":
                            self.gomel(driver, client)

                        if city.title == "Center-Grodno":
                            self.grodno(driver, client)

                        if city.title == "Center-Lida":
                            self.lida(driver, client)

                        if city.title == "Center-Minsk":
                            self.minsk(driver, client)

                        if city.title == "Center-Mogilev":
                            self.mogilev(driver, client)

                        if city.title == "Center-Pinsk":
                            self.baranovichi(driver, client)

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

    def baranovichi(self, driver, client):
        element = driver.find_element(By.ID, "mat-select-0")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)
        try:
            driver.find_element(By.ID, "mat-option-0").click()
            time.sleep(5)

            driver.find_element(By.ID, "mat-select-2").click()
            time.sleep(5)

            # national_visa_element = driver.find_element(By.XPATH, f"//span[text()=' {NATIONAL} ']")
            if client.visa_type == "National Visa D":
                driver.find_element(By.ID, "mat-option-246").click()
                time.sleep(3)
                driver.find_element(By.ID, "mat-select-4").click()
                time.sleep(3)
                if client.visa_sub_category == 'Driver D-visa':
                    driver.find_element(By.ID, "mat-option-248").click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Karta Polaka D-visa':
                    driver.find_element(By.ID, "mat-option-249").click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Other D-visa':
                    driver.find_element(By.ID, "mat-option-250").click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Postal D-visa':
                    driver.find_element(By.ID, "mat-option-251").click()
                    time.sleep(2)
                elif client.visa_sub_category == 'Work D-visa':
                    driver.find_element(By.ID, "mat-option-252").click()
                    time.sleep(2)

                date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                          'input[formcontrolname="dateOfBirth"].form-control')
                date_of_birth_input.clear()
                date_of_birth_input.send_keys(client.date_of_birth)

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
                driver.find_element(By.ID, "mat-option-247").click()
                time.sleep(3)
                date_of_birth_input = driver.find_element(By.CSS_SELECTOR,
                                                          'input[formcontrolname="dateOfBirth"].form-control')
                date_of_birth_input.clear()
                date_of_birth_input.send_keys(client.date_of_birth)
                time.sleep(3)
                driver.find_element(By.ID, "mat-select-6").click()
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

    def brest(self, driver, client):
        pass

    def gomel(self, driver, client):
        pass

    def grodno(self, driver, client):
        pass

    def lida(self, driver, client):
        pass

    def minsk(self, driver, client):
        pass

    def mogilev(self, driver, client):
        pass

    def pinsk(self, driver, client):
        pass

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
                            f"//span[contains(@class, 'mat-option-text') and text()=' {gender_option} ']").click()
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
        print('xxx')
