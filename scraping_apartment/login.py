from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class LoginHandler:
    def __init__(self, driver, wait, email, password):
        self.driver = driver
        self.wait = wait
        self.email = email
        self.password = password

    def open_login_form(self):
        time.sleep(3)
        try:
            print("Looking for login button...", flush=True)
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/a"))
            )
            login_button.click()
            print("✅ Login button clicked", flush=True)
            time.sleep(2)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"⚠️ Could not open login form: {e}", flush=True)
            raise e

    def fill_credentials(self):
        try:
            print("Filling in login credentials...", flush=True)
            email_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/form/div[1]/div/label/input"))
            )
            email_field.clear()
            email_field.send_keys(self.email)
            print("✅ Email entered", flush=True)

            password_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/form/div[2]/div/label/input"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            print("✅ Password entered", flush=True)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"⚠️ Error filling credentials: {e}", flush=True)
            raise e

    def submit_form(self):
        try:
            print("Submitting login form...", flush=True)
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/form/div[4]/button"))
            )
            submit_button.click()
            print("✅ Login form submitted", flush=True)
            time.sleep(2)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"⚠️ Error submitting login form: {e}", flush=True)
            raise e

    def login(self):
        try:
            self.open_login_form()
            self.fill_credentials()
            self.submit_form()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"⚠️ Error finalizing login form: {e}", flush=True)
            raise e
