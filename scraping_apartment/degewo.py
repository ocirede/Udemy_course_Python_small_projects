from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class Degewo:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def handle_cookies(self):
        try:
            cookies_button = self.driver.find_element(By.ID, "cookie-consent-submit-all")
            self.driver.execute_script("arguments[0].click();", cookies_button)
            print("🍪 Cookies accepted")
            time.sleep(1)
        except NoSuchElementException:
            pass

    def open_kontakt(self, main_window):
        try:
            kontakt_link = self.driver.find_element(By.XPATH, ".//a[contains(@href, '#kontakt')]")
            self.driver.execute_script("arguments[0].click();", kontakt_link)
            print("➡️ Kontakt link clicked")
            time.sleep(2)
            return True
        except NoSuchElementException:
            print("⚠️ Kontakt link not found")
            self.driver.close()
            self.driver.switch_to.window(main_window)
            return False

    def switch_to_iframe(self, main_window):
        try:
            iframe = self.driver.find_element(By.XPATH, "//iframe[contains(@src, 'app.wohnungshelden.de')]")
            self.driver.switch_to.frame(iframe)
            time.sleep(1)
            print("🟢 Switched to iframe")
            return True
        except NoSuchElementException:
            print("⚠️ Iframe not found")
            self.driver.close()
            self.driver.switch_to.window(main_window)
            return False

    def select_gender(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, ".ng-select-container").click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Frau']"))).click()
            print("👩 Gender selected: Frau")
            time.sleep(2)
        except Exception as e:
            print("⚠️ Gender selection error:", e)

    def fill_personal_info(self, vorname, nachname, email, telephone):
        self.wait.until(EC.element_to_be_clickable((By.ID, "firstName"))).send_keys(vorname)
        self.wait.until(EC.element_to_be_clickable((By.ID, "lastName"))).send_keys(nachname)
        self.wait.until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(email)
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.ant-input.ng-untouched.ng-pristine.ng-invalid"))
        ).send_keys(telephone)
        print("📩 Personal info filled")
        time.sleep(1)

    def fill_kids_field(self):
        try:
            kids_input = self.wait.until(EC.element_to_be_clickable((By.ID, "formly_3_input_kids_1")))
            kids_input.clear()
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
                kids_input, "1")
            print("✅ Kids field filled")
        except:
            print("⚠️ Kids number option not available, skipping...")

    def fill_people_field(self, people):
        try:
            persons_input = self.wait.until(EC.element_to_be_clickable((By.ID, "formly_3_input_numberPersonsTotal_0")))
            persons_input.clear()
            persons_input.send_keys(people)
            print("👥 People field filled")
            time.sleep(1)
        except:
            print("⚠️ People number option not available, skipping...")

    def handle_wbs(self, date):
        ja_wbs_elements = self.driver.find_elements(By.ID, "formly_4_radio_$$_wbs_available_$$_0-Ja")
        if ja_wbs_elements:
            self.driver.execute_script("arguments[0].click();", ja_wbs_elements[0])
            self.wait.until(
                EC.element_to_be_clickable((By.ID, "formly_5_input_$$_wbs_valid_until_$$_0"))
            ).send_keys(date)
            print("🏠 WBS clicked")
        else:
            print("⚠️ WBS option not available, skipping WBS step...")

    def fill_rooms_field(self, people):
        try:
            rooms_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "formly_5_select_$$_wbs_max_number_rooms_$$_1"))
            )
            rooms_input.send_keys(people)
            print("🟢 Rooms input focused")
            time.sleep(1)

            visible_filtered = [
                opt for opt in self.driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option") if
                opt.is_displayed()
            ]
            if visible_filtered:
                self.driver.execute_script("arguments[0].click();", visible_filtered[1])
                print("✅ WBS type selected")
            else:
                print("⚠️ No visible options for rooms")
        except Exception as e:
            print(f"⚠️ Rooms option not available, skipping... ({e})")

    def fill_income_field(self):
        try:
            income_input = self.wait.until(
                EC.element_to_be_clickable((By.ID, "formly_4_input_$$_monthly_net_income_$$_0")))
            income_input.clear()
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
                income_input, "14.500")
            print("✅ Income field filled")
            time.sleep(1)
        except:
            print("⚠️ Income number option not available, skipping...")

    def select_self_option(self):
        for n in range(9):
            try:
                wrapper_id = f"formly_{n}_select_degewo_fuer_wen_ist_wohnungsanfrage_0"
                elements = self.driver.find_elements(By.ID, wrapper_id)
                if not elements:
                    continue
                element = elements[0]
                element.send_keys("selbst")
                visible_filtered = [
                    opt for opt in self.driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option") if
                    opt.is_displayed()
                ]
                if visible_filtered:
                    self.driver.execute_script("arguments[0].click();", visible_filtered[0])
                    print("✅ 'Für mich selbst' selected")
                    break
            except Exception as e:
                print(f"❌ Error selecting 'Für mich selbst': {e}")

    def submit_form(self, ):
        try:
            submit_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy='btn-submit']")))
            self.driver.execute_script("arguments[0].click();", submit_btn)
            print("✅ Application sent successfully")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error submitting thr form: {e}")



    def dewego_applying(self, vorname, nachname, email, telephone, date, people, main_window):
        """
                Executes the full Degewo housing application process with safety checks.
                Returns True if completed successfully, False otherwise.
                """
        try:
            print("🚀 Starting Degewo form process")
            self.handle_cookies()
            if not self.open_kontakt(main_window):
                return False
            if not self.switch_to_iframe(main_window):
                return False
            self.select_gender()
            self.fill_personal_info(vorname, nachname, email, telephone)
            self.fill_kids_field()
            self.fill_people_field(people)
            self.handle_wbs(date)
            self.fill_rooms_field(people)
            self.fill_income_field()
            self.select_self_option()
            self.submit_form()

            print("✅ Degewo process finished")

        except Exception as e:
            print("⚠️ Unexpected error in dewego_applying:", e)
            return False



