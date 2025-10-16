from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

class WBM:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    # 1️⃣ Handle cookie banner
    def handle_cookies(self):
        try:
            accept_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cm-btn-success"))
            )
            accept_btn.click()
            print("🍪 Cookie banner accepted")
        except Exception:
            print("⚠️ Cookie banner not found or already dismissed")

    # 2️⃣ Open contact form
    def open_contact_form(self):
        try:
            submit_link = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.openimmo-detail__contact-box-button.btn.scrollLink"))
            )
            submit_link.click()
            print("➡️ 'Anfrage absenden' button clicked")
            time.sleep(2)
        except Exception:
            print("⚠️ Could not click 'Anfrage absenden' button")

    # 3️⃣ Wait for form to appear
    def wait_for_form(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "article#c722 form.powermail_form"))
            )
            print("🟢 Powermail form is now visible")
        except Exception:
            print("⚠️ Powermail form did not appear")

    # 4️⃣ Fill WBS info
    def fill_wbs_info(self, date):
        try:
            ja_label = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='powermail_field_wbsvorhanden_1']"))
            )
            self.driver.execute_script("arguments[0].click();", ja_label)
            print("☑️ 'WBS vorhanden: ja' label clicked")
            time.sleep(1)

            date_input = self.wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_wbsgueltigbis")))
            date_input.clear()
            date_input.send_keys(date)
            print("☑️ 'WBS gültig bis' date input filled")

            select_zimmer = self.wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_wbszimmeranzahl")))
            select_zimmer.click()
            zimmer_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[text()='2']")))
            self.driver.execute_script("arguments[0].selected = true;", zimmer_option)
            print("☑️ 'WBS Zimmeranzahl' option selected")

            option_wbs = self.wait.until(EC.element_to_be_clickable(
                (By.ID, "powermail_field_einkommensgrenzenacheinkommensbescheinigung9")
            ))
            option_wbs.click()
            wbs_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[text()='WBS 100']")))
            wbs_option.click()
            print("☑️ 'Einkommensgrenze WBS' option selected")

        except Exception as e:
            print("⚠️ Could not fill WBS info:", e)

    # 5️⃣ Fill personal info
    def fill_personal_info(self, vorname, nachname, email):
        try:
            anrede = self.wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_anrede")))
            anrede.click()
            frau_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[text()='Frau']")))
            frau_option.click()
            print("☑️ 'Anrede' option selected")

            self.driver.find_element(By.ID, "powermail_field_name").send_keys(nachname)
            print("☑️ 'Nachname' input filled")

            self.driver.find_element(By.ID, "powermail_field_vorname").send_keys(vorname)
            print("☑️ 'Vorname' input filled")

            self.driver.find_element(By.ID, "powermail_field_e_mail").send_keys(email)
            print("☑️ 'E-Mail' input filled")

        except Exception as e:
            print("⚠️ Could not fill personal info:", e)

    # 6️⃣ Click Datenschutz checkbox
    def click_privacy(self):
        try:
            checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_datenschutzhinweis_1")))
            self.driver.execute_script("arguments[0].click();", checkbox)
            print("☑️ Datenschutz checkbox clicked")
        except Exception:
            print("⚠️ Could not click Datenschutz checkbox")

    # 7️⃣ Submit form
    def submit_form(self):
        try:
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.col-sm-offset-2 > button.btn.btn-primary[type='submit']")
            ))
            submit_button.click()
            print("✅ Form submitted: 'Anfrage absenden' clicked")
        except Exception as e:
            print("⚠️ Could not submit the form:", e)

    # 8️⃣ Master function
    def wbm_applying(self, vorname, nachname, email, date):
        try:
            print("🚀 Starting WBM form process")
            self.handle_cookies()
            self.open_contact_form()
            self.wait_for_form()
            self.fill_wbs_info(date)
            self.fill_personal_info(vorname, nachname, email)
            self.click_privacy()
            self.submit_form()
            print("✅ WBM process completed successfully")
            return True
        except Exception as e:
            print(f"⚠️ Unexpected error in WBM process: {e}")
            return False
