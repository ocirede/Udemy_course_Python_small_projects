from selenium import webdriver
import tempfile
from selenium.webdriver.support.ui import WebDriverWait

class Chrome:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        #self.chrome_options.add_argument("--headless=new")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.tmp_profile = tempfile.mkdtemp(prefix="chrome-selenium-")
        self.chrome_options.add_argument(f"--user-data-dir={self.tmp_profile}")
        self.chrome_options.add_argument("--remote-debugging-port=9222")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("https://www.inberlinwohnen.de/")
        self.wait = WebDriverWait(self.driver, 15)
