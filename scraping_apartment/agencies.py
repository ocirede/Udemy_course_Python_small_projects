from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from urls_processed_load import UrlLoaded
from save_url import SaveUrl
from degewo import Degewo
from gewobag import Gewobag
from howoge import Howoge
from stadt_und_land import StadtLand
from wbm import WBM

class Agencies:
    def __init__(self, driver, wait, vorname, nachname, email, telephone, date, people):
        self.condition_met = True
        self.i = 0
        self.block_index = 0
        self.driver = driver
        self.wait = wait
        self.vorname = vorname
        self.nachname = nachname
        self.email = email
        self.telephone = telephone
        self.date = date
        self.people = people
        url_loader = UrlLoaded()
        save_url = SaveUrl()
        self.urls_list = url_loader.load_processed_urls()
        self.save_url = save_url.save_url
        degewo = Degewo(self.driver, self.wait)
        self.degewo = degewo.dewego_applying
        gewobag = Gewobag(self.driver, self. wait)
        self.gewobag = gewobag.gewobag_applying
        howoge = Howoge(self.driver, self.wait)
        self.howoge = howoge.howoge_applying
        stadt_und_land = StadtLand(self.driver, self.wait)
        self.stadt_und_land = stadt_und_land.stadt_und_land_applying
        wbm = WBM(self.driver, self.wait)
        self.wbm = wbm.wbm_applying

    def check_condition(self):
        return self.condition_met

    def run_main_loop(self):
        self.i = 0
        while self.check_condition():
            print(f"Loop iteration {self.i}")
            select_elements = self.driver.find_elements(
                By.XPATH,
                "/html/body/main/div[2]/div[2]/section[2]/div/div[3]/div/div[2]/div/label/select/option"
            )

            if self.i >= len(select_elements):
                break

            option = select_elements[self.i]
            agency_name = option.text.strip()
            print(f"Current agency: {agency_name}")

            # Skip invalid ones
            if agency_name in ["... zeige alle Gesellschaften", "Wohnungen der GESOBAU"]:
                self.i += 1
                continue

            # Click agency and wait for results to load
            option.click()
            time.sleep(2)
            self.run_apartments_loop(agency_name)
            print(f"✅ Finished processing {agency_name}")
            self.i += 1
        print("🎉 All agencies processed")

    def run_apartments_loop(self, agency_name):
        urls = self.urls_list
        save_url = self.save_url
        degewo = self.degewo
        gewobag = self.gewobag
        howoge = self.howoge
        stadt_und_land = self.stadt_und_land
        wbm = self.wbm
        self.block_index = 0

        while self.check_condition():
            apartment_blocks = self.driver.find_elements(By.CSS_SELECTOR, "div[id^='apartment']")
            if not apartment_blocks:
                print("⚠️ No apartments found on this page")
                break

            districts = [
                "Marzahn-Hellersdorf", "Tempelhof-Schöneberg",
                "Friedrichshain-Kreuzberg", "Lichtenberg", "Pankow", "Mitte"
            ]
            while self.block_index < len(apartment_blocks):
                try:
                    main_window = self.driver.current_window_handle
                    block = apartment_blocks[self.block_index]

                    span = block.find_element(By.CSS_SELECTOR, "span.block")
                    text = span.text.strip()
                    print("Found apartment:", text)

                    if "2,0 Zimmer" in text and any(d in text for d in districts):
                        print("✅ Matching apartment:", text)
                        try:
                            try:
                                print("🔍 Checking for details button...")
                                button = block.find_element(By.CSS_SELECTOR, "button")
                                print(f"✅ Found button: {button.text}")
                                self.driver.execute_script("arguments[0].click();", button)
                                time.sleep(1)
                            except Exception as e:
                                print(f"⚠️ No details button found ({e}), checking WBS...")
                            try:
                                wbs_text = block.find_element(
                                    By.XPATH,
                                    ".//dt[contains(text(), 'WBS')]/following-sibling::dd[1]"
                                ).text.strip()
                                print(f"🔍 Found WBS text: {wbs_text}")
                                if wbs_text != "erforderlich" or wbs_text == "unbekannt":
                                    print(f"❌ WBS is '{wbs_text}', skipping")
                                    self.block_index += 1
                                    continue
                            except Exception as e:
                                print(f"⚠️ WBS info not found ({e}), skipping")
                                self.block_index += 1
                                continue

                            print("✅ WBS required, proceeding")

                            apartment_link = block.find_element(By.CSS_SELECTOR, "a")
                            print(f"🔗 Clicking apartment link: {apartment_link.get_attribute('href')}")
                            self.driver.execute_script("arguments[0].click();", apartment_link)
                            time.sleep(1)
                            new_window = [w for w in self.driver.window_handles if w != main_window][0]
                            self.driver.switch_to.window(new_window)

                        except Exception as e:
                            print(f"⚠️ Could not open apartment: {e}")
                            self.block_index += 1
                            continue

                        # Process apartment page
                        og_url = self.driver.current_url
                        print("url", og_url)
                        if og_url in urls:
                            print(f"⚠️ Duplicate URL found, skipping: {og_url}")
                        else:
                            urls.append(og_url)
                            save_url(og_url)

                            # Call agency-specific function
                            if agency_name == "Wohnungen der degewo":
                                degewo(self.vorname, self.nachname, self.email, self.telephone, self.date, self.people,  main_window)
                            elif agency_name == "Wohnungen der Gewobag":
                                 gewobag(self.vorname, self.nachname, self.email, self.telephone, self.date, self.people,  main_window)
                            elif agency_name == "Wohnungen der HOWOGE":
                                 howoge(self.vorname, self.nachname, self.email, main_window)
                            elif agency_name == "Wohnungen der STADT UND LAND":
                                 stadt_und_land(self.vorname, self.nachname, self.email, self.telephone)
                            elif agency_name == "Wohnungen der WBM":
                                 wbm(self.vorname, self.nachname, self.email, self.telephone)

                        # Safely close tab and switch back
                        current = self.driver.current_window_handle
                        if current != main_window:
                            self.driver.close()
                            print("🗙 Closed detail tab")
                        if main_window in self.driver.window_handles:
                            self.driver.switch_to.window(main_window)
                            print("🔄 Back to main window")

                        # Refresh apartment blocks
                        apartment_blocks = self.driver.find_elements(By.CSS_SELECTOR, "div[id^='apartment']")

                    else:
                        print("❌ Skipping, apartment doesn't match the criteria:", text)

                except Exception as e:
                    print(f"Error processing apartment block: {e}")
                    try:
                        if main_window in self.driver.window_handles:
                            self.driver.switch_to.window(main_window)
                    except:
                        pass

                self.block_index += 1

            # Pagination
            try:
                next_button = self.driver.find_element(By.XPATH, "//button[.//span[text()='Vor']]")
                if next_button.is_enabled():
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)
                    print("➡️ Going to next page")

                    self.block_index = 0
                    apartment_blocks = self.driver.find_elements(By.CSS_SELECTOR, "div[id^='apartment']")
                else:
                    print("⛔ No more pages for this agency")
                    break
            except NoSuchElementException:
                print("❌ Next page button not found, finishing agency")
                break







