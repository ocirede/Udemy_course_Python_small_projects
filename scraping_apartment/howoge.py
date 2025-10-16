from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class Howoge:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def handle_cookies(self):
        # 1. Handle cookie banner if present
        try:
            shadow_host = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cmpwrapper"))
            )
            button = self.driver.execute_script("""
                         return arguments[0].shadowRoot.querySelector('a.cmpboxbtnno');
                     """, shadow_host)
            if button:
                button.click()
                print("🍪 Cookie banner closed")
        except TimeoutException:
            pass

    def contact_button(self):
        try:
            link = self.driver.find_element(By.XPATH, ".//a[contains(text(),'Besichtigung vereinbaren')]")
            self.driver.execute_script("arguments[0].click();", link)
            print("➡️ Clicked Besichtigung vereinbaren")
        except NoSuchElementException:
            print("⚠️ No link found for this apartment")
            return

    def switch_to_iframe(self, main_window):
        time.sleep(2)
        windows = self.driver.window_handles
        new_window = None
        for w in windows:
            if w != main_window:
                new_window = w
                break
        if not new_window:
            print("⚠️ No new window found")
            return
        self.driver.switch_to.window(new_window)


    def sending_form(self, vorname, nachname, email):
        try:
            # First checkbox
            checkbox_text = "Ja, ich habe die Hinweise zum WBS zur Kenntnis genommen."
            label = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{checkbox_text}')]"))
            )
            clickable_div = label.find_element(By.CSS_SELECTOR, ".form-checkbox--box")
            self.driver.execute_script("arguments[0].click();", clickable_div)
            print("☑️ Checkbox 1 clicked")

            # Weiter button
            weiter_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[data-process-next='2']"))
            )
            self.driver.execute_script("arguments[0].click();", weiter_button)
            print("➡️ Weiter clicked (1)")

            # Second checkbox
            checkbox_text2 = "Ja, ich habe den Hinweis zum Haushaltsnettoeinkommen zur Kenntnis genommen."
            label2 = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{checkbox_text2}')]"))
            )
            clickable_div2 = label2.find_element(By.CSS_SELECTOR, ".form-checkbox--box")
            self.driver.execute_script("arguments[0].click();", clickable_div2)
            print("☑️ Checkbox 2 clicked")

            weiter_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[data-process-next='3']"))
            )
            self.driver.execute_script("arguments[0].click();", weiter_button)
            print("➡️ Weiter clicked (2)")

            # Third checkbox
            checkbox_text3 = "Ja, ich habe den Hinweis zur Bonitätsauskunft zur Kenntnis genommen."
            label3 = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{checkbox_text3}')]"))
            )
            clickable_div3 = label3.find_element(By.CSS_SELECTOR, ".form-checkbox--box")
            self.driver.execute_script("arguments[0].click();", clickable_div3)
            print("☑️ Checkbox 3 clicked")

            weiter_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[data-process-next='4']"))
            )
            self.driver.execute_script("arguments[0].click();", weiter_button)
            print("➡️ Weiter clicked (3)")

            # Fill personal data
            name = self.driver.find_element(By.ID, "immo-form-firstname")
            name.send_keys(vorname)
            surname = self.driver.find_element(By.ID, "immo-form-lastname")
            surname.send_keys(nachname)
            mail = self.driver.find_element(By.ID, "immo-form-email")
            mail.send_keys(email)

            weiter_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "button.button.primary[data-process-submit='data-process-submit']"))
            )
            self.driver.execute_script("arguments[0].click();", weiter_button)
            print("🎉 Application sent successfully")

        except Exception as e:
            print("⚠️ Error in form:", e)

    def howoge_applying(self, vorname, nachname, email, main_window):
        """
        Executes the full Howoge housing application process safely.
        Returns True if completed successfully, False otherwise.
        """
        try:
            print("🚀 Starting Howoge form process")

            # Step 1: Handle cookies
            try:
                self.handle_cookies()
            except Exception as e:
                print("⚠️ Cookie handling failed:", e)

            # Step 2: Click on the 'Besichtigung vereinbaren' button
            try:
                self.contact_button()
            except Exception as e:
                print("⚠️ Could not click contact button:", e)
                return False

            # Step 3: Switch to iframe / new window
            try:
                self.switch_to_iframe(main_window)
            except Exception as e:
                print("⚠️ Window switch failed:", e)
                return False

            # Step 4: Fill and send the form
            try:
                self.sending_form(vorname, nachname, email)
            except Exception as e:
                print("⚠️ Error while sending form:", e)
                return False

            print("✅ Howoge process completed successfully")
            return True

        except Exception as e:
            print("⚠️ Unexpected outer error:", e)
            time.sleep(3)
            return False
