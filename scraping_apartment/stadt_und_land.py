from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time


class StadtLand:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # 1️⃣ Handle cookies
    def handle_cookies(self):
        try:
            host = self.driver.find_element(By.ID, "cmpwrapper")
            shadow_root = self.driver.execute_script("return arguments[0].shadowRoot", host)
            no_button = shadow_root.find_element(By.CSS_SELECTOR, "#cmpwelcomebtnno a")
            if no_button:
                no_button.click()
                print("🍪 Cookie banner closed")
        except (TimeoutException, NoSuchElementException):
            print("⚠️ No cookie banner found, continuing")

    # 2️⃣ Check if apartment is senior-friendly
    def check_seniorengerecht(self):
        try:
            senior = self.driver.find_element(
                By.XPATH, "//tr[th[normalize-space()='Seniorengerecht']]/td[normalize-space()='Ja']"
            )
            print("✅ This apartment is Seniorengerecht (Yes)")
            return True
        except NoSuchElementException:
            print("⚠️ 'Seniorengerecht: Ja' not found")
            return False

    # 3️⃣ Fill the form fields
    def fill_form(self, vorname, nachname, phone, email):
        try:
            self.driver.find_element(By.NAME, "name").send_keys(vorname)
            print("☑️ First name entered")
        except Exception as e:
            print("⚠️ Could not enter first name:", e)

        try:
            self.driver.find_element(By.NAME, "surname").send_keys(nachname)
            print("☑️ Last name entered")
        except Exception as e:
            print("⚠️ Could not enter last name:", e)

        try:
            self.driver.find_element(By.NAME, "phone").send_keys(phone)
            print("☑️ Phone number entered")
        except Exception as e:
            print("⚠️ Could not enter phone number:", e)

        try:
            self.driver.find_element(By.NAME, "email").send_keys(email)
            print("☑️ Email entered")
        except Exception as e:
            print("⚠️ Could not enter email:", e)

    # 4️⃣ Click checkboxes
    def click_checkboxes(self):
        try:
            self.driver.find_element(By.NAME, "privacy").click()
            print("☑️ Privacy checkbox clicked")
        except Exception as e:
            print("⚠️ Could not click privacy checkbox:", e)

        try:
            self.driver.find_element(By.NAME, "provision").click()
            print("☑️ Provision checkbox clicked")
        except Exception as e:
            print("⚠️ Could not click provision checkbox:", e)

    # 5️⃣ Submit the form
    def submit_form(self):
        try:
            button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_button__primary__FME8s"))
            )
            button.click()
            print("📨 Form submitted successfully")
        except Exception:
            # fallback click
            try:
                button = self.driver.find_element(By.CSS_SELECTOR, "button.Button_button__primary__FME8s")
                actions = ActionChains(self.driver)
                actions.move_to_element(button).click().perform()
                print("✅ Form submitted (fallback)")
            except Exception as e:
                print("⚠️ Could not submit form:", e)

    # 6️⃣ Master function
    def stadt_und_land_applying(self, vorname, nachname, email, phone):
        try:
            print("🚀 Starting Stadt und Land form process")
            self.handle_cookies()

            is_senior = self.check_seniorengerecht()
            if is_senior:
                print("⏭️ Skipping form because apartment is for Seniorengerecht")
                return False

            self.fill_form(vorname, nachname, phone, email)
            self.click_checkboxes()
            self.submit_form()

            print("✅ Stadt und Land process completed successfully")
            return True

        except Exception as e:
            print("⚠️ Unexpected outer error:", e)
            time.sleep(3)
            return False
