
import time
import os
from dotenv import load_dotenv
import sys
import traceback

from chrome import Chrome
from cookies import Cookies
from login import LoginHandler
from personal_portal import PortalHandler
from agencies import Agencies

print("=" * 80, flush=True)
print("SCRIPT STARTING - FIRST LINE OF CODE", flush=True)
print(f"Python version: {sys.version}", flush=True)
print(f"Current working directory: {os.getcwd()}", flush=True)
print("=" * 80, flush=True)
sys.stdout.flush()

load_dotenv()

VORNAME = os.getenv("VORNAME")
NACHNAME = os.getenv("NACHNAME")
TELEPHONE =  os.getenv("TELEPHONE")
PEOPLE = os.getenv("PEOPLE")
DATE = os.getenv("DATE")
APPLYING_EMAIL = os.getenv("EMAIL")
WBS_PASSWORD = os.getenv("WBS_PASSWORD")
INBERLINWOHNEN_URL = "https://www.inberlinwohnen.de/"

print("Environment variables loaded", flush=True)
print("Creating Chrome options...", flush=True)


chrome = Chrome()

tmp_profile = chrome.tmp_profile

print(f"Temporary profile created at: {tmp_profile}", flush=True)
print("Initializing Chrome driver...", flush=True)

driver = chrome.driver
print("✅ Driver initialized!", flush=True)

print(f"Navigating to {INBERLINWOHNEN_URL}...", flush=True)
chrome.open_page(INBERLINWOHNEN_URL)
print("✅ Page loaded!", flush=True)

# Continue with your wait and agency_options_function() call
print("About to start main scraping logic...", flush=True)

wait = chrome.wait

time.sleep(2)

cookies = Cookies(chrome.driver, chrome.wait)
login = LoginHandler(chrome.driver, chrome.wait, APPLYING_EMAIL, WBS_PASSWORD)
portal = PortalHandler(chrome.driver, chrome.wait)
agencies = Agencies(chrome.driver, chrome.wait, VORNAME, NACHNAME, APPLYING_EMAIL, TELEPHONE, DATE, PEOPLE)


if __name__ == "__main__":
    try:
        print("Starting cookies_function()...", flush=True)
        print("✅ cookies_function() completed", flush=True)
        cookies.accept_all()
        print("Starting login_function()...", flush=True)
        login.login()
        print("✅ login_function() completed", flush=True)

        print("Starting personal_portal...", flush=True)
        portal.personal_portal_access()
        print("✅ personal_portal completed", flush=True)

        print("Starting agency_options_function()...", flush=True)
        agencies.run_main_loop()
        print("✅ agency_options_function() completed", flush=True)

    except Exception as e:
        print("=" * 80, flush=True)
        print(f"⚠️ EXCEPTION CAUGHT: {type(e).__name__}", flush=True)
        print(f"⚠️ Error message: {str(e)}", flush=True)
        print("=" * 80, flush=True)
        traceback.print_exc()
        sys.stdout.flush()
    finally:
        try:
            driver.quit()
        except:
            pass
        print("✅ Script finished. driver closed.", flush=True)

