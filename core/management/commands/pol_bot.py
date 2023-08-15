import threading
import time

from django.core.management import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import LOGIN_URL, NATIONAL, OTHER
from core.models import Client

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
            user = users_from_db[user_id % len(users_from_db)]
            email = user.reg_email
            password = user.reg_password
            thread = threading.Thread(target=self.login_user_and_simulate_activity,
                                      args=(driver, user_id, email, password))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def login_user_and_simulate_activity(self, driver, user_id, email, password):
        try:
            if len(driver.window_handles) <= user_id:
                driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[user_id])

            # login
            driver.get(LOGIN_URL)
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.ID, "mat-input-0"))
            )
            driver.find_element(By.ID, "mat-input-0").send_keys(email)
            time.sleep(2)
            driver.find_element(By.ID, "mat-input-1").send_keys(password)
            time.sleep(2)
            # wait 10 min
            WebDriverWait(driver, 600).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.fs-24.fs-sm-46.mb-25"))
            )
            time.sleep(3)
            while True:
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

                        # try:
                        #     continue_button = driver.find_element(
                        #         By.XPATH,
                        #         "//button[contains(@class, 'mat-raised-button') and contains(@class, 'mat-button-disabled')]"
                        #     )
                        #     time.sleep(3)
                        #     if continue_button.is_displayed() and continue_button.get_attribute("disabled") == "False":
                        #         continue_button.click()
                        #         print("Button has been unlocked and pressed")
                        #     else:
                        #         print("The button is either not visible or enabled")
                        #     time.sleep(5)
                        # except Exception:
                        #     print("The button is disabled")

                    except Exception as e:
                        print(e)

        except Exception as e:
            print(f"User {user_id} error: {e}")
