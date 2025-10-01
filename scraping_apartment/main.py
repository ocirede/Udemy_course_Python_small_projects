from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from dotenv import load_dotenv
import tempfile

load_dotenv()

VORNAME = os.getenv("VORNAME")
NACHNAME = os.getenv("NACHNAME")
TELEPHONE =  os.getenv("TELEPHONE")
PEOPLE = os.getenv("PEOPLE")
DATE = os.getenv("DATE")
APPLYING_EMAIL = os.getenv("EMAIL")
WBS_PASSWORD = os.getenv("WBS_PASSWORD")
URL = os.getenv("URL")

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")


tmp_profile = tempfile.mkdtemp(prefix="chrome-selenium-")
chrome_options.add_argument(f"--user-data-dir={tmp_profile}")

chrome_options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

wait = WebDriverWait(driver, 15)



def cookies_function():
    try:
        alles_akzeptieren = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div[4]/button[2]")))
        alles_akzeptieren.click()
    except (NoSuchElementException, TimeoutException) as e:
        return f"{e}"

def login_function():
    time.sleep(2)
    try:
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH,  "/html/body/div[1]/div/div/div/div[2]/div/a")))
        login_button.click()
        time.sleep(2)
        email_login = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/form/div[1]/div/label/input")))
        email_login.send_keys(APPLYING_EMAIL)
        password_login = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/form/div[2]/div/label/input")))
        password_login.send_keys(WBS_PASSWORD)
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/form/div[4]/button")))
        login_btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        return f"{e}"

def personal_portal_function():
    time.sleep(2)
    try:
        persönlicher_wohnungsfinder = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[2]/div[5]/a")))
        persönlicher_wohnungsfinder.click()
    except (NoSuchElementException, TimeoutException) as e:
        return f"{e}"

def agency_options_function():
    urls_list = load_processed_urls()

    # Get all agency options
    option_count = len(driver.find_elements(
        By.XPATH,
        "/html/body/main/div[2]/div[2]/section[2]/div/div[3]/div/div[2]/div/label/select/option"
    ))

    for i in range(option_count):
        # Re-query options each iteration to avoid stale element references
        select_elements = driver.find_elements(
            By.XPATH,
            "/html/body/main/div[2]/div[2]/section[2]/div/div[3]/div/div[2]/div/label/select/option"
        )
        option = select_elements[i]
        agency_name = option.text.strip()
        print(f"Current agency: {agency_name}")

        if agency_name in ["... zeige alle Gesellschaften", "Wohnungen der GESOBAU"]:
            continue

        option.click()
        time.sleep(2)

        while True:
            # Re-query apartment blocks fresh every page iteration
            apartment_blocks = driver.find_elements(By.CSS_SELECTOR, "div[id^='apartment']")
            if not apartment_blocks:
                print("⚠️ No apartments found on this page")
                break

            districts = ["Marzahn-Hellersdorf", "Tempelhof-Schöneberg",
                         "Friedrichshain-Kreuzberg", "Lichtenberg", "Pankow", "Mitte"]

            block_index = 0
            while block_index < len(apartment_blocks):
                try:
                    main_window = driver.current_window_handle
                    block = apartment_blocks[block_index]

                    # Get span text safely
                    span = block.find_element(By.CSS_SELECTOR, "span.block")
                    text = span.text.strip()
                    print("Found apartment:", text)

                    # Filter apartments
                    if "2,0 Zimmer" in text and any(d in text for d in districts):
                        print("✅ Matching apartment:", text)

                        # Find the buttons relative to the block
                        try:
                            button = block.find_element(By.CSS_SELECTOR, "button")
                            driver.execute_script("arguments[0].click();", button)
                            time.sleep(1)

                            # Find the single WBS dd element in this block
                            wbs_element = block.find_element(By.XPATH,".//dt[contains(text(), 'WBS')]/following-sibling::dd[1]")
                            wbs_text = wbs_element.text.strip()

                            if wbs_text != "erforderlich":
                                print(f"❌ WBS is '{wbs_text}', skipping")
                                block_index += 1
                                continue

                            print("✅ WBS required, proceeding")

                            # Click apartment link
                            apartment_link = block.find_element(By.CSS_SELECTOR, "a")
                            driver.execute_script("arguments[0].click();", apartment_link)
                            time.sleep(3)

                        except Exception as e:
                            print(f"⚠️ Could not click apartment button/link: {e}")
                            block_index += 1
                            continue


                        # Switch to new window
                        new_windows = [w for w in driver.window_handles if w != main_window]
                        if not new_windows:
                            print("⚠️ No new window opened for this apartment, skipping...")
                            block_index += 1
                            continue

                        driver.switch_to.window(new_windows[0])
                        og_url = driver.current_url

                        if og_url in urls_list:
                            print(f"⚠️ Duplicate URL found, skipping: {og_url}")
                            driver.close()
                            driver.switch_to.window(main_window)

                        else:
                            urls_list.append(og_url)
                            save_url(og_url)

                            if agency_name == "Wohnungen der degewo":
                                degewo_function(main_window)
                            elif agency_name == "Wohnungen der Gewobag":
                                gewobag_function(main_window)
                            elif agency_name == "Wohnungen der HOWOGE":
                                howoge_function(main_window)
                            elif agency_name == "Wohnungen der STADT UND LAND":
                                stadt_und_land_function()
                            elif agency_name == "Wohnungen der WBM":
                                wbm_function()

                        # Re-query apartment blocks after DOM update (in case DOM changed)
                        apartment_blocks = driver.find_elements(By.CSS_SELECTOR, "div[id^='apartment']")

                    else:
                        print("❌ Skipping, apartment doesnt match the criteria :", text)

                except Exception as e:
                    print(f"Error processing apartment block: {e}")
                    try:
                        driver.close()
                        driver.switch_to.window(main_window)
                    except:
                        pass

                # Always increment block_index at the end, regardless of what happened
                block_index += 1

            # Pagination: click "Vor" for next page
            try:
                next_button = driver.find_element(By.XPATH, "//button[.//span[text()='Vor']]")
                if next_button.is_enabled():
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)
                    print("➡️ Going to next page")
                else:
                    print("⛔ No more pages for this agency")
                    break
            except NoSuchElementException:
                print("❌ Next page button not found, finishing agency")
                break

def degewo_function(main_window):
    try:
        # 1️⃣ Handle cookies if present
        try:
            cookies_button = driver.find_element(By.ID, "cookie-consent-submit-all")
            driver.execute_script("arguments[0].click();", cookies_button)
            print("🍪 Cookies accepted")
            time.sleep(1)
        except NoSuchElementException:
            pass

        # 2️⃣ Click Kontakt link
        try:
            kontakt_link = driver.find_element(By.XPATH, ".//a[contains(@href, '#kontakt')]")
            driver.execute_script("arguments[0].click();", kontakt_link)
            print("➡️ Kontakt link clicked")
            time.sleep(2)
        except NoSuchElementException:
            print("⚠️ Kontakt link not found")
            driver.close()
            driver.switch_to.window(main_window)
            return

        # 3️⃣ Switch to iframe
        try:
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'app.wohnungshelden.de')]")
            driver.switch_to.frame(iframe)
            time.sleep(1)
            print("🟢 Switched to iframe")
        except NoSuchElementException:
            print("⚠️ Iframe not found")
            driver.close()
            driver.switch_to.window(main_window)
            return

        # 4️⃣ Gender selection
        try:
            driver.find_element(By.CSS_SELECTOR, ".ng-select-container").click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Frau']"))).click()
            time.sleep(2)
        except Exception as e:
            print("⚠️ Gender selection error:", e)

        # 5️⃣ Fill personal info
        wait.until(EC.element_to_be_clickable((By.ID, "firstName"))).send_keys(VORNAME)
        wait.until(EC.element_to_be_clickable((By.ID, "lastName"))).send_keys(NACHNAME)
        wait.until(EC.element_to_be_clickable((By.ID, "email"))).send_keys(APPLYING_EMAIL)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.ant-input.ng-untouched.ng-pristine.ng-invalid"))).send_keys(TELEPHONE)
        time.sleep(1)

        # 6️⃣ Number of persons
        persons_input = wait.until(EC.element_to_be_clickable((By.ID, "formly_3_input_numberPersonsTotal_0")))
        persons_input.clear()
        persons_input.send_keys(PEOPLE)
        time.sleep(1)

        # 7️⃣ Optional WBS
        ja_wbs_elements = driver.find_elements(By.ID, "formly_4_radio_$$_wbs_available_$$_0-Ja")
        if ja_wbs_elements:
            driver.execute_script("arguments[0].click();", ja_wbs_elements[0])
            wait.until(EC.element_to_be_clickable((By.ID, "formly_5_input_$$_wbs_valid_until_$$_0"))).send_keys(DATE)
            rooms_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "formly_5_select_$$_wbs_max_number_rooms_$$_1")))
            driver.execute_script("arguments[0].click();", rooms_dropdown)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='2']"))).click()
            print("🏠 WBS filled")
        else:
            print("⚠️ WBS option not available, skipping WBS step...")

        # 8️⃣ Kids field
        kids_input = wait.until(EC.element_to_be_clickable((By.ID, "formly_3_input_kids_1")))
        kids_input.clear()
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", kids_input, "1")
        print("✅ kids field filled")

        # 9️⃣ Income field
        income_input = wait.until(EC.element_to_be_clickable((By.ID, "formly_4_input_$$_monthly_net_income_$$_0")))
        income_input.clear()
        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", income_input, "14.500")
        print("✅ Einkommen field filled")
        time.sleep(1)

        # 1️⃣0️⃣ Select 'Für mich selbst'
        wrapper = driver.find_element(By.ID, "formly_6_select_degewo_fuer_wen_ist_wohnungsanfrage_0_wrapper")
        driver.execute_script("arguments[0].click();", wrapper)
        print("🟢 Wrapper clicked")

        driver.switch_to.default_content()
        try:
            panel = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ng-dropdown-panel")))
            options = panel.find_elements(By.CSS_SELECTOR, ".ng-option")
            for opt in options:
                label = opt.find_element(By.CSS_SELECTOR, "span.ng-option-label").text.strip()
                if label == "Für mich selbst":
                    driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", opt)
                    print("✅ Selected 'Für mich selbst'")
                    break
        except TimeoutException:
            print("⚠️ Dropdown panel never appeared")
            driver.switch_to.frame(iframe)  # back to iframe

        # 1️⃣1️⃣ Submit form
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy='btn-submit']")))
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(3)

        # 1️⃣2️⃣ Check duplicate email
        try:
            error_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//nz-alert[@nztype='error']//span[contains(@class, 'ant-alert-message')]"))
            )
            if "E-Mail" in error_message.text or "Anfrage" in error_message.text:
                print("❌ Email already exists:", error_message.text)
        except TimeoutException:
            print("✅ Form submitted successfully for:", APPLYING_EMAIL)

        except Exception as e:
            print("⚠️ Error in form:", e)

        finally:
            driver.close()
            driver.switch_to.window(main_window)
            print("🔄 Back to main window")
            time.sleep(1)

    except Exception as e:
        print("⚠️ Unexpected error in form:", e)

def gesobau_function(main_window):
    try:
        jetzt_bewerben_btn = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/main/article/section[2]/section[2]/div/div/span/a")
        jetzt_bewerben_btn.click()
        if not jetzt_bewerben_btn:
            pass

    except Exception as e:
        print("⚠️ Error submitting form:", e)

def gewobag_function(main_window):
    try:
        # --- Cookies ---
        try:
            cookies_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/div[3]/div/div[2]")
            ))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cookies_button)
            cookies_button.click()
            print("✅ Cookies accepted")
        except TimeoutException:
            print("ℹ️ No cookies popup")

        # --- Anfragen senden ---
        try:
            anfragen_senden_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[2]/div/main/article/div[2]/div/div[1]/button[5]")
            ))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", anfragen_senden_btn)
            anfragen_senden_btn.click()
            print("✅ 'Anfragen senden' clicked")
            time.sleep(2)
        except Exception as e:
            print("⚠️ Error clicking 'Anfragen senden':", e)
            return

        # --- Switch to iframe ---
        try:
            iframe = driver.find_element(By.ID, "contact-iframe")
            driver.switch_to.frame(iframe)
            print("✅ Switched to iframe")
        except Exception as e:
            print("⚠️ Error switching to iframe:", e)
            return

        # --- Salutation ---
        try:
            anrede = wait.until(EC.element_to_be_clickable((By.ID, "salutation-dropdown")))
            anrede.click()
            time.sleep(1)
            frau = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Frau']")))
            frau.click()
            print("✅ Salutation selected")
        except Exception as e:
            print("⚠️ Error selecting salutation:", e)

        # --- Personal info ---
        for field_id, value, desc in [
            ("firstName", VORNAME, "Vorname"),
            ("lastName", NACHNAME, "Nachname"),
            ("email", APPLYING_EMAIL, "Email")
        ]:
            try:
                elem = wait.until(EC.element_to_be_clickable((By.ID, field_id)))
                elem.clear()
                elem.send_keys(value)
                print(f"✅ {desc} filled")
                time.sleep(0.5)
            except Exception as e:
                print(f"⚠️ Error filling {desc}:", e)

        # --- Adults / Children combined field ---
        try:
            # try individual fields first
            try:
                anzahl_erwachsene = driver.find_element(By.CSS_SELECTOR, "input[id*='anzahl_erwachsene']")
                anzahl_erwachsene.clear()
                anzahl_erwachsene.send_keys("1")
                print("✅ Anzahl Erwachsene filled")
            except NoSuchElementException:
                print("ℹ️ Anzahl Erwachsene not found")

            try:
                anzahl_kinder = driver.find_element(By.CSS_SELECTOR, "input[id*='anzahl_kinder']")
                anzahl_kinder.clear()
                anzahl_kinder.send_keys("1")
                print("✅ Anzahl Kinder filled")
            except NoSuchElementException:
                print("ℹ️ Anzahl Kinder not found")

            # fallback to combined field
            combined_field = driver.find_element(By.CSS_SELECTOR, "input[id*='gesamtzahl_der_einziehenden']")
            combined_field.clear()
            combined_field.send_keys(PEOPLE)
            print("✅ Combined adult+children field filled")
        except Exception as e:
            print("⚠️ Error filling adults/children fields:", e)

        # --- WBS section ---
        try:
            # Find WBS radio with multiple selectors
            selectors = [
                "input[id*='wbs_available_'][type='radio']",
                "input[name*='wbs'][type='radio']",
                "label[for*='wbs'] input[type='radio']"
            ]

            ja_wbs_elements = None
            for selector in selectors:
                ja_wbs_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if ja_wbs_elements:
                    break

            if ja_wbs_elements:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ja_wbs_elements[0])
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", ja_wbs_elements[0])
                print("✅ 'WBS Ja' clicked")
                time.sleep(1)

                try:
                    wbs_date = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id*='wbs_valid_until']")))
                    wbs_date.clear()
                    wbs_date.send_keys(DATE)
                    print("✅ WBS validity date filled")
                except Exception:
                    print("⚠️ WBS validity date not found")

                # --- WBS type selection ---
                try:
                    wbs_dropdown = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[id*='art_bezeichnung_des_wbs']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", wbs_dropdown)

                    print(
                        f"DEBUG: WBS dropdown found, tag: {wbs_dropdown.tag_name}, id: {wbs_dropdown.get_attribute('id')}")

                    # Try clicking the arrow wrapper
                    try:
                        arrow = wbs_dropdown.find_element(By.CSS_SELECTOR, ".ng-arrow-wrapper")
                        driver.execute_script("arguments[0].click();", arrow)
                        print("DEBUG: Clicked arrow wrapper")
                    except:
                        driver.execute_script("arguments[0].click();", wbs_dropdown)
                        print("DEBUG: Clicked main container")

                    time.sleep(3)

                    # Find the listbox elements and examine them
                    listboxes = driver.find_elements(By.CSS_SELECTOR, "[role='listbox']")
                    print(f"DEBUG: Found {len(listboxes)} listboxes")

                    for i, listbox in enumerate(listboxes):
                        try:
                            # Check if this listbox is related to our dropdown
                            listbox_id = listbox.get_attribute('id')
                            aria_expanded = listbox.get_attribute('aria-expanded')
                            print(
                                f"  Listbox {i}: id='{listbox_id}', aria-expanded='{aria_expanded}', visible={listbox.is_displayed()}")

                            # Look for options within this listbox
                            options_in_listbox = listbox.find_elements(By.XPATH, "./*")
                            print(f"    Child elements in listbox {i}: {len(options_in_listbox)}")

                            for j, child in enumerate(options_in_listbox[:3]):
                                try:
                                    child_tag = child.tag_name
                                    child_text = child.text.strip()
                                    child_class = child.get_attribute('class')
                                    child_role = child.get_attribute('role')
                                    print(
                                        f"      Child {j}: tag='{child_tag}', text='{child_text[:30]}', class='{child_class}', role='{child_role}'")

                                    # Check if this looks like a WBS option
                                    if child_text and (
                                            'wbs' in child_text.lower() or 'berechtigt' in child_text.lower()):
                                        print(f"        >>> POTENTIAL WBS OPTION FOUND: '{child_text}'")
                                        try:
                                            driver.execute_script("arguments[0].click();", child)
                                            print("✅ WBS type selected via listbox child")
                                            break
                                        except Exception as click_err:
                                            print(f"        Failed to click: {click_err}")
                                except Exception as child_err:
                                    print(f"      Child {j}: Error examining - {child_err}")

                        except Exception as listbox_err:
                            print(f"  Listbox {i}: Error examining - {listbox_err}")

                    # Alternative approach: try typing to filter options
                    try:
                        # Find the input field within the dropdown
                        input_field = wbs_dropdown.find_element(By.CSS_SELECTOR, "input")
                        input_field.send_keys("WBS")
                        time.sleep(1)
                        print("DEBUG: Typed 'WBS' into input field")

                        # Now look for filtered options
                        filtered_options = driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option")
                        visible_filtered = [opt for opt in filtered_options if opt.is_displayed()]
                        print(f"DEBUG: {len(visible_filtered)} visible filtered options")

                        if visible_filtered:
                            driver.execute_script("arguments[0].click();", visible_filtered[0])
                            print("✅ WBS type selected via typing")
                        else:
                            print("⚠️ No visible options after typing")

                    except Exception as type_err:
                        print(f"DEBUG: Typing approach failed: {type_err}")
                        print("⚠️ WBS type option not found")

                except Exception as e:
                    print("⚠️ WBS type dropdown not found or could not select:", e)

                # --- Rooms selection ---
                try:
                    # Use the exact ID we found in the debug output
                    raume_dropdown = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[id*='wbs_max_number_rooms']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", raume_dropdown)

                    print(f"DEBUG: Rooms dropdown found, id: {raume_dropdown.get_attribute('id')}")

                    # Click the arrow wrapper
                    try:
                        arrow = raume_dropdown.find_element(By.CSS_SELECTOR, ".ng-arrow-wrapper")
                        driver.execute_script("arguments[0].click();", arrow)
                        print("DEBUG: Clicked rooms arrow wrapper")
                    except:
                        driver.execute_script("arguments[0].click();", raume_dropdown)
                        print("DEBUG: Clicked rooms main container")

                    time.sleep(2)

                    # Try typing approach that worked for WBS
                    try:
                        input_field = raume_dropdown.find_element(By.CSS_SELECTOR, "input")
                        input_field.clear()
                        input_field.send_keys("2")
                        time.sleep(1)
                        print("DEBUG: Typed '2' into rooms input field")

                        # Look for filtered options
                        filtered_options = driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option")
                        visible_filtered = [opt for opt in filtered_options if opt.is_displayed()]
                        print(f"DEBUG: {len(visible_filtered)} visible room options after typing")

                        # Show what options we found
                        for i, option in enumerate(visible_filtered[:3]):
                            try:
                                text = option.text.strip()
                                print(f"  Room Option {i}: '{text}'")
                            except:
                                pass

                        # Try to find the 2 rooms option - prefer exact match
                        room_option = None
                        exact_match = None
                        partial_match = None

                        for option in visible_filtered:
                            try:
                                text = option.text.strip()
                                text_lower = text.lower()

                                # Look for exact "2 räume" match first
                                if text_lower == "2 räume":
                                    exact_match = option
                                    print(f"DEBUG: Found exact match: '{text}'")
                                    break
                                # Look for options containing "2" and "räume"
                                elif '2' in text_lower and 'räume' in text_lower and not partial_match:
                                    partial_match = option
                                    print(f"DEBUG: Found partial match: '{text}'")
                            except:
                                continue

                        room_option = exact_match or partial_match

                        if room_option:
                            driver.execute_script("arguments[0].click();", room_option)
                            print("✅ Rooms selected via typing")
                        elif visible_filtered:
                            # If we can't find exact match, try the first option
                            driver.execute_script("arguments[0].click();", visible_filtered[0])
                            print("✅ First room option selected")
                        else:
                            print("⚠️ No visible room options after typing")

                    except Exception as type_err:
                        print(f"DEBUG: Typing approach failed for rooms: {type_err}")
                        print("⚠️ Rooms option not found")

                except Exception as e:
                    print("⚠️ Rooms dropdown not found or could not select:", e)

            else:
                print("❌ WBS radio elements not found")

        except Exception as e:
            print(f"❌ WBS section failed: {e}")

        # --- Person dropdown ---
        try:
            # Use ng-select instead of select, based on the debug output
            person_dropdown = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "ng-select[id*='fuer_wen_wird_die_wohnungsanfrage_gestellt']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", person_dropdown)

            print(f"DEBUG: Person dropdown found, id: {person_dropdown.get_attribute('id')}")

            # Click the arrow wrapper to open dropdown
            try:
                arrow = person_dropdown.find_element(By.CSS_SELECTOR, ".ng-arrow-wrapper")
                driver.execute_script("arguments[0].click();", arrow)
                print("DEBUG: Clicked person arrow wrapper")
            except:
                driver.execute_script("arguments[0].click();", person_dropdown)
                print("DEBUG: Clicked person main container")

            time.sleep(2)

            # Use typing approach that worked for WBS
            try:
                input_field = person_dropdown.find_element(By.CSS_SELECTOR, "input")
                input_field.clear()
                input_field.send_keys("mich")  # Type "mich" to filter for "Für mich selbst"
                time.sleep(1)
                print("DEBUG: Typed 'mich' into person input field")

                # Look for filtered options
                filtered_options = driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option")
                visible_filtered = [opt for opt in filtered_options if opt.is_displayed()]
                print(f"DEBUG: {len(visible_filtered)} visible person options after typing")

                # Show what options we found
                for i, option in enumerate(visible_filtered[:3]):
                    try:
                        text = option.text.strip()
                        print(f"  Person Option {i}: '{text}'")
                    except:
                        pass

                # Try to find the "Für mich selbst" option
                person_option = None
                for option in visible_filtered:
                    try:
                        text = option.text.strip().lower()
                        if 'mich' in text and 'selbst' in text:
                            person_option = option
                            print(f"DEBUG: Found matching person option: '{option.text.strip()}'")
                            break
                    except:
                        continue

                if person_option:
                    driver.execute_script("arguments[0].click();", person_option)
                    print("✅ 'Für mich selbst' selected via typing")
                elif visible_filtered:
                    # If we can't find exact match, try the first option
                    driver.execute_script("arguments[0].click();", visible_filtered[0])
                    print("✅ First person option selected")
                else:
                    print("⚠️ No visible person options after typing")

            except Exception as type_err:
                print(f"DEBUG: Typing approach failed for person: {type_err}")
                print("⚠️ Person option not found")

        except Exception as e:
            print("⚠️ Could not select person option:", e)

        # --- Telephone ---
        try:
            telephone = driver.find_element(By.CSS_SELECTOR, "input[id*='telephone_number']")
            telephone.clear()
            telephone.send_keys(TELEPHONE)
            print("✅ Telephone filled")
        except Exception as e:
            print("⚠️ Error filling telephone:", e)

        # --- Datenschutzhinweis ---
        try:
            checkbox = driver.find_element(By.CSS_SELECTOR, "input[id*='datenschutzhinweis']")
            if not checkbox.is_selected():
                checkbox.click()
            print("✅ Datenschutzhinweis clicked")
        except Exception as e:
            print("⚠️ Error clicking Datenschutzhinweis:", e)

        # --- Submit ---
        try:
            # Try multiple selectors for submit button
            submit_selectors = [
                "button[id*='btn-submit']",
                "input[id*='btn-submit']",
                "button[type='submit']",
                "input[type='submit']",
                "button[class*='submit']",
                "button[class*='btn-primary']",
                "button[class*='btn-success']",
                "*[value*='submit' i]",
                "*[value*='absenden' i]",
                "button:contains('Submit')",
                "button:contains('Absenden')",
                "button:contains('Weiter')"
            ]

            submit_btn = None
            used_selector = None

            for selector in submit_selectors:
                try:
                    submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    used_selector = selector
                    print(f"DEBUG: Submit button found with selector: {selector}")
                    break
                except:
                    continue

            # If CSS selectors didn't work, try XPath
            if not submit_btn:
                xpath_selectors = [
                    "//button[contains(text(), 'Submit')]",
                    "//button[contains(text(), 'Absenden')]",
                    "//button[contains(text(), 'Weiter')]",
                    "//input[@type='submit']",
                    "//button[@type='submit']",
                    "//button[contains(@class, 'submit')]",
                    "//button[contains(@id, 'submit')]"
                ]

                for xpath in xpath_selectors:
                    try:
                        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                        used_selector = xpath
                        print(f"DEBUG: Submit button found with XPath: {xpath}")
                        break
                    except:
                        continue

            if submit_btn:
                # Get button details for debugging
                try:
                    btn_id = submit_btn.get_attribute('id')
                    btn_class = submit_btn.get_attribute('class')
                    btn_text = submit_btn.text.strip()
                    btn_value = submit_btn.get_attribute('value')
                    btn_type = submit_btn.get_attribute('type')

                    print(
                        f"DEBUG: Button details - ID: '{btn_id}', Class: '{btn_class}', Text: '{btn_text}', Value: '{btn_value}', Type: '{btn_type}'")
                except:
                    print("DEBUG: Could not get button details")

                # Scroll to button and click
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
                time.sleep(0.5)

                # Try multiple click strategies
                click_success = False

                # Strategy 1: JavaScript click
                try:
                    driver.execute_script("arguments[0].click();", submit_btn)
                    print("✅ Form submitted (JavaScript click)")
                    click_success = True
                except Exception as js_err:
                    print(f"DEBUG: JavaScript click failed: {js_err}")

                    # Strategy 2: Regular click
                    try:
                        submit_btn.click()
                        print("✅ Form submitted (regular click)")
                        click_success = True
                    except Exception as reg_err:
                        print(f"DEBUG: Regular click failed: {reg_err}")

                        # Strategy 3: ActionChains click
                        try:
                            actions = ActionChains(driver)
                            actions.move_to_element(submit_btn).click().perform()
                            print("✅ Form submitted (ActionChains click)")
                            click_success = True
                        except Exception as action_err:
                            print(f"DEBUG: ActionChains click failed: {action_err}")

                if not click_success:
                    print("⚠️ All click strategies failed")
            else:
                print("⚠️ Submit button not found with any selector")

                # Debug: Show all buttons on page
                try:
                    all_buttons = driver.find_elements(By.TAG_NAME, "button")
                    all_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='submit'], input[type='button']")

                    print(f"DEBUG: Found {len(all_buttons)} button elements and {len(all_inputs)} submit/button inputs")

                    for i, btn in enumerate((all_buttons + all_inputs)[:5]):
                        try:
                            btn_id = btn.get_attribute('id') or 'no-id'
                            btn_class = btn.get_attribute('class') or 'no-class'
                            btn_text = btn.text.strip() or btn.get_attribute('value') or 'no-text'
                            print(f"  Button {i}: ID='{btn_id}', Class='{btn_class[:30]}', Text='{btn_text[:30]}'")
                        except:
                            pass
                except:
                    print("DEBUG: Could not enumerate buttons")

        except Exception as e:
            print("⚠️ Error submitting form:", e)
    finally:
        try:
            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(main_window)
            print("✅ Switched back to main window")
        except Exception as e:
            print("⚠️ Error switching back:", e)

        time.sleep(2)

def howoge_function(main_window):
    try:
        # 1. Handle cookie banner if present
        try:
            shadow_host = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cmpwrapper"))
            )
            button = driver.execute_script("""
                return arguments[0].shadowRoot.querySelector('a.cmpboxbtnno');
            """, shadow_host)
            if button:
                button.click()
                print("🍪 Cookie banner closed")
        except TimeoutException:
            pass

        # 3. Click "Besichtigung vereinbaren"
        try:
            link = driver.find_element(By.XPATH, ".//a[contains(text(),'Besichtigung vereinbaren')]")
            driver.execute_script("arguments[0].click();", link)
            print("➡️ Clicked Besichtigung vereinbaren")
        except NoSuchElementException:
            print("⚠️ No link found for this apartment")
            return

        # 4. Switch to new window
        time.sleep(2)
        windows = driver.window_handles
        new_window = None
        for w in windows:
            if w != main_window:
                new_window = w
                break
        if not new_window:
            print("⚠️ No new window found")
            return
        driver.switch_to.window(new_window)

        # === FORM PROCESS ===
        try:
            # First checkbox
            checkbox_text = "Ja, ich habe die Hinweise zum WBS zur Kenntnis genommen."
            label = wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{checkbox_text}')]"))
            )
            clickable_div = label.find_element(By.CSS_SELECTOR, ".form-checkbox--box")
            driver.execute_script("arguments[0].click();", clickable_div)
            print("☑️ Checkbox 1 clicked")

            # Weiter button
            weiter_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[data-process-next='2']"))
            )
            driver.execute_script("arguments[0].click();", weiter_button)
            print("➡️ Weiter clicked (1)")

            # Second checkbox
            checkbox_text2 = "Ja, ich habe den Hinweis zum Haushaltsnettoeinkommen zur Kenntnis genommen."
            label2 = wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{checkbox_text2}')]"))
            )
            clickable_div2 = label2.find_element(By.CSS_SELECTOR, ".form-checkbox--box")
            driver.execute_script("arguments[0].click();", clickable_div2)
            print("☑️ Checkbox 2 clicked")

            weiter_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[data-process-next='3']"))
            )
            driver.execute_script("arguments[0].click();", weiter_button)
            print("➡️ Weiter clicked (2)")

            # Third checkbox
            checkbox_text3 = "Ja, ich habe den Hinweis zur Bonitätsauskunft zur Kenntnis genommen."
            label3 = wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{checkbox_text3}')]"))
            )
            clickable_div3 = label3.find_element(By.CSS_SELECTOR, ".form-checkbox--box")
            driver.execute_script("arguments[0].click();", clickable_div3)
            print("☑️ Checkbox 3 clicked")

            weiter_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[data-process-next='4']"))
            )
            driver.execute_script("arguments[0].click();", weiter_button)
            print("➡️ Weiter clicked (3)")

            # Fill personal data
            vorname = driver.find_element(By.ID, "immo-form-firstname")
            vorname.send_keys(VORNAME)
            nachname = driver.find_element(By.ID, "immo-form-lastname")
            nachname.send_keys(NACHNAME)
            email = driver.find_element(By.ID, "immo-form-email")
            email.send_keys(APPLYING_EMAIL)

            weiter_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary[data-process-submit='data-process-submit']"))
            )
            driver.execute_script("arguments[0].click();", weiter_button)
            print("🎉 Application sent successfully")

        except Exception as e:
            print("⚠️ Error in form:", e)

        finally:
            # 5. Close new window and return to main
            driver.close()
            driver.switch_to.window(main_window)
            print("🔄 Back to main window")

    except Exception as e:
        print("⚠️ Unexpected outer error:", e)
        time.sleep(3)

def stadt_und_land_function():
    try:
        is_seniorengerecht = False
        try:
            host = driver.find_element(By.ID, "cmpwrapper")
            shadow_root = driver.execute_script("return arguments[0].shadowRoot", host)
            no_button = shadow_root.find_element(By.CSS_SELECTOR, "#cmpwelcomebtnno a")
            if no_button:
                no_button.click()
                print("🍪 Cookie banner closed")
        except TimeoutException:
            pass
        try:
            senior = driver.find_element(
                By.XPATH, "//tr[th[normalize-space()='Seniorengerecht']]/td[normalize-space()='Ja']"
            )
            print("✅ This apartment is Seniorengerecht (Yes)")
            is_seniorengerecht = True
        except NoSuchElementException:
            print("⚠️ 'Seniorengerecht: Ja' not found")

        if not is_seniorengerecht:

            try:
                vorname = driver.find_element(By.NAME, "name")
                vorname.send_keys(VORNAME)
                print("☑️ First name entered")
            except Exception as e:
                print("⚠️ Could not enter first name:", e)

            try:
                nachname = driver.find_element(By.NAME, "surname")
                nachname.send_keys(NACHNAME)
                print("☑️ Last name entered")
            except Exception as e:
                print("⚠️ Could not enter last name:", e)

            try:
                phone = driver.find_element(By.NAME, "phone")
                phone.send_keys(TELEPHONE)
                print("☑️ Phone number entered")
            except Exception as e:
                print("⚠️ Could not enter phone number:", e)

            try:
                email = driver.find_element(By.NAME, "email")
                email.send_keys(APPLYING_EMAIL)
                print("☑️ Email entered")
            except Exception as e:
                print("⚠️ Could not enter email:", e)

            try:
                privacy = driver.find_element(By.NAME, "privacy")
                privacy.click()
                print("☑️ Privacy checkbox clicked")
            except Exception as e:
                print("⚠️ Could not click privacy checkbox:", e)

            try:
                provision = driver.find_element(By.NAME, "provision")
                provision.click()
                print("☑️ Provision checkbox clicked")
            except Exception as e:
                print("⚠️ Could not click provision checkbox:", e)

            try:
                button = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_button__primary__FME8s")))
                button.click()
            except:
                actions = ActionChains(driver)
                actions.move_to_element(button).click().perform()
        else:
            print("⏭️ Skipping form because apartment is for Seniorengerecht")

    except Exception as e:
        print("⚠️ Unexpected outer error:", e)
        time.sleep(3)

def wbm_function():
    try:
        try:
            accept_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cm-btn-success"))
            )
            accept_btn.click()
            print("🍪 Cookie banner accepted")
        except Exception as e:
            print("⚠️ Cookie banner not found or already dismissed:", e)

        try:
            submit_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.openimmo-detail__contact-box-button.btn.scrollLink"))
            )
            submit_link.click()
            print("➡️ 'Anfrage absenden' button clicked")
            time.sleep(2)
        except Exception as e:
            print("⚠️ Could not click 'Anfrage absenden' button:", e)

        try:
            form = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "article#c722 form.powermail_form"))
            )
            print("🟢 Powermail form is now visible")
        except Exception as e:
            print("⚠️ Powermail form did not appear:", e)

        try:
            ja_label = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='powermail_field_wbsvorhanden_1']"))
            )
            driver.execute_script("arguments[0].click();", ja_label)
            print("☑️ 'WBS vorhanden: ja' label clicked")
            time.sleep(2)
        except Exception as e:
            print("⚠️ Could not click 'WBS vorhanden: ja' label:", e)

        try:
            date_input = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_wbsgueltigbis")))
            date_input.clear()
            date_input.send_keys("06/30/2026")
            print("☑️ 'WBS gültig bis' date input filled")
        except Exception as e:
            print("⚠️ Could not fill 'WBS gültig bis' date input:", e)

        try:
            select_zimmer = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_wbszimmeranzahl")))
            select_zimmer.click()
            zimmer_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[text()='2']")))
            driver.execute_script("arguments[0].selected = true;", zimmer_option)
            print("☑️ 'WBS Zimmeranzahl' option selected")
        except Exception as e:
            print("⚠️ Could not select 'WBS Zimmeranzahl' option:", e)

        try:
            option_wbs = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_einkommensgrenzenacheinkommensbescheinigung9")))
            option_wbs.click()
            wbs_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[text()='WBS 100']")))
            wbs_option.click()
            print("☑️ 'Einkommensgrenze WBS' option selected")
        except Exception as e:
            print("⚠️ Could not select 'Einkommensgrenze WBS' option:", e)

        try:
            anrede = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_anrede")))
            anrede.click()
            frau_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//option[text()='Frau']")))
            frau_option.click()
            print("☑️ 'Anrede' option selected")
        except Exception as e:
            print("⚠️ Could not select 'Anrede' option:", e)

        try:
            nachname = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_name")))
            nachname.send_keys(NACHNAME)
            print("☑️ 'Nachname' input filled")
        except Exception as e:
            print("⚠️ Could not fill 'Nachname' input:", e)

        try:
            vorname = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_vorname")))
            vorname.send_keys(VORNAME)
            print("☑️ 'Vorname' input filled")
        except Exception as e:
            print("⚠️ Could not fill 'Vorname' input:", e)

        try:
            email = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_e_mail")))
            email.send_keys(APPLYING_EMAIL)
            print("☑️ 'E-Mail' input filled")
        except Exception as e:
            print("⚠️ Could not fill 'E-Mail' input:", e)

        try:
            checkbox = wait.until(EC.element_to_be_clickable((By.ID, "powermail_field_datenschutzhinweis_1")))
            driver.execute_script("arguments[0].click();", checkbox)
            print("☑️ Datenschutz checkbox clicked")
        except Exception as e:
            print("⚠️ Could not click Datenschutz checkbox:", e)
        try:
            submit_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.col-sm-offset-2 > button.btn.btn-primary[type='submit']")))
            submit_button.click()
            print("✅ Form submitted: 'Anfrage absenden' clicked")
        except Exception as e:
            print("⚠️ Could not submit the form:", e)

    except Exception as e:
        print(f"Unexpected error in wbm_function: {e}")

def load_processed_urls():
    try:
        with open('processed_urls.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_url(url):
    with open('processed_urls.txt', 'a') as f:
        f.write(url + '\n')

if __name__ == "__main__":
    try:
        cookies_function()

        login_function()

        personal_portal_function()

        agency_options_function()

    except Exception as e:
        print(f"⚠️ Unexpected error in main: {e}")
    finally:
        driver.quit()
        print("✅ Script finished. driver closed.")


