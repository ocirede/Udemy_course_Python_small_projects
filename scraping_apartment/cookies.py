from chrome import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class Cookies:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def accept_all(self):
        try:
            print("Looking for cookie banner...", flush=True)
            alles_akzeptieren = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[4]/button[2]")))
            alles_akzeptieren.click()
            print("✅ Cookie banner accepted", flush=True)
        except (NoSuchElementException, TimeoutException):
            print("⚠️ No cookie banner (headless mode) - continuing", flush=True)
            # No return - just pass through
