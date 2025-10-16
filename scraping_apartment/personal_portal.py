from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class PortalHandler:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def personal_portal_access(self):
        time.sleep(2)
        try:
            print("Looking for personal portal link...", flush=True)
            personal_portal = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[2]/div[5]/a")))
            personal_portal.click()
            print("✅ Personal portal opened", flush=True)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"⚠️ Personal portal error: {e}", flush=True)
            return f"{e}"