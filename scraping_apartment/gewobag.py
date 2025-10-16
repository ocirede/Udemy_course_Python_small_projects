from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

class Gewobag:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def handle_cookies(self):
        try:
            cookies_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 "/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/div[1]/div[3]/div/div[2]")
            ))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cookies_button)
            cookies_button.click()
            print("✅ Cookies accepted")
        except TimeoutException:
            print("ℹ️ No cookies popup")

    def form_button(self):
        try:
            anfragen_senden_btn = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.rental-contact")
            ))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", anfragen_senden_btn)
            anfragen_senden_btn.click()
            print("✅ 'Anfragen senden' clicked")
            time.sleep(2)
        except Exception as e:
            print("⚠️ Error clicking 'Anfragen senden':", e)
            return

    def switch_to_iframe(self, main_window):
        try:
            iframe = self.driver.find_element(By.ID, "contact-iframe")
            self.driver.switch_to.frame(iframe)
            print("✅ Switched to iframe")
        except Exception as e:
            print("⚠️ Error switching to iframe:", e)
            self.driver.close()
            self.driver.switch_to.window(main_window)
            return

    def personal_infos(self, vorname, nachname, email):
        try:
            anrede = self.wait.until(EC.element_to_be_clickable((By.ID, "salutation-dropdown")))
            anrede.click()
            time.sleep(1)
            frau = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-label='Frau']")))
            frau.click()
            print("✅ Salutation selected")
        except Exception as e:
            print("⚠️ Error selecting salutation:", e)

        for field_id, value, desc in [
            ("firstName", vorname, "Vorname"),
            ("lastName", nachname, "Nachname"),
            ("email", email, "Email")
        ]:
            try:
                elem = self.wait.until(EC.element_to_be_clickable((By.ID, field_id)))
                elem.clear()
                elem.send_keys(value)
                print(f"✅ {desc} filled")
                time.sleep(0.5)
            except Exception as e:
                print(f"⚠️ Error filling {desc}:", e)

    def total_people(self, people):
        try:
            try:
                anzahl_erwachsene = self.driver.find_element(By.CSS_SELECTOR, "input[id*='anzahl_erwachsene']")
                anzahl_erwachsene.clear()
                anzahl_erwachsene.send_keys("1")
                print("✅ Anzahl Erwachsene filled")
            except NoSuchElementException:
                print("ℹ️ Anzahl Erwachsene not found")

            try:
                anzahl_kinder = self.driver.find_element(By.CSS_SELECTOR, "input[id*='anzahl_kinder']")
                anzahl_kinder.clear()
                anzahl_kinder.send_keys("1")
                print("✅ Anzahl Kinder filled")
            except NoSuchElementException:
                print("ℹ️ Anzahl Kinder not found")

            # fallback to combined field
            combined_field = self.driver.find_element(By.CSS_SELECTOR, "input[id*='gesamtzahl_der_einziehenden']")
            combined_field.clear()
            combined_field.send_keys(people)
            print("✅ Combined adult+children field filled")
        except Exception as e:
            print("⚠️ Error filling adults/children fields:", e)

    def wbs_selection(self, date):
        try:
            selectors = [
                "input[id*='wbs_available_'][type='radio']",
                "input[name*='wbs'][type='radio']",
                "label[for*='wbs'] input[type='radio']"
            ]

            ja_wbs_elements = None
            for selector in selectors:
                ja_wbs_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if ja_wbs_elements:
                    break

            if ja_wbs_elements:
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ja_wbs_elements[0])
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", ja_wbs_elements[0])
                print("✅ 'WBS Ja' clicked")
                time.sleep(1)

                try:
                    wbs_date = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id*='wbs_valid_until']")))
                    wbs_date.clear()
                    wbs_date.send_keys(date)
                    print("✅ WBS validity date filled")
                except Exception:
                    print("⚠️ WBS validity date not found")

                # --- WBS type selection ---
                try:
                    wbs_dropdown = self.wait.until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "ng-select[id*='art_bezeichnung_des_wbs']"))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", wbs_dropdown)

                    print(
                        f"DEBUG: WBS dropdown found, tag: {wbs_dropdown.tag_name}, id: {wbs_dropdown.get_attribute('id')}")

                    # Try clicking the arrow wrapper
                    try:
                        arrow = wbs_dropdown.find_element(By.CSS_SELECTOR, ".ng-arrow-wrapper")
                        self.driver.execute_script("arguments[0].click();", arrow)
                        print("DEBUG: Clicked arrow wrapper")
                    except:
                        self.driver.execute_script("arguments[0].click();", wbs_dropdown)
                        print("DEBUG: Clicked main container")

                    time.sleep(3)

                    # Find the listbox elements and examine them
                    listboxes = self.driver.find_elements(By.CSS_SELECTOR, "[role='listbox']")
                    print(f"DEBUG: Found {len(listboxes)} listboxes")

                    for i, listbox in enumerate(listboxes):
                        try:
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
                                            self.driver.execute_script("arguments[0].click();", child)
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
                        filtered_options = self.driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option")
                        visible_filtered = [opt for opt in filtered_options if opt.is_displayed()]
                        print(f"DEBUG: {len(visible_filtered)} visible filtered options")

                        if visible_filtered:
                            self.driver.execute_script("arguments[0].click();", visible_filtered[0])
                            print("✅ WBS type selected via typing")
                        else:
                            print("⚠️ No visible options after typing")

                    except Exception as type_err:
                        print(f"DEBUG: Typing approach failed: {type_err}")
                        print("⚠️ WBS type option not found")

                except Exception as e:
                    print("⚠️ WBS type dropdown not found or could not select:", e)
            else:
                print("❌ WBS radio elements not found")
        except Exception as e:
            print(f"⚠️ Error in wbs_selection: {e}")

    def room_selection(self):
        try:
            raume_dropdown = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[id*='wbs_max_number_rooms']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", raume_dropdown)

            print(f"DEBUG: Rooms dropdown found, id: {raume_dropdown.get_attribute('id')}")

            try:
                arrow = raume_dropdown.find_element(By.CSS_SELECTOR, ".ng-arrow-wrapper")
                self.driver.execute_script("arguments[0].click();", arrow)
                print("DEBUG: Clicked rooms arrow wrapper")
            except:
                self.driver.execute_script("arguments[0].click();", raume_dropdown)
                print("DEBUG: Clicked rooms main container")

            time.sleep(2)

            try:
                input_field = raume_dropdown.find_element(By.CSS_SELECTOR, "input")
                input_field.clear()
                input_field.send_keys("2")
                time.sleep(1)
                print("DEBUG: Typed '2' into rooms input field")

                # Look for filtered options
                filtered_options = self.driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option")
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
                    self.driver.execute_script("arguments[0].click();", room_option)
                    print("✅ Rooms selected via typing")
                elif visible_filtered:
                    # If we can't find exact match, try the first option
                    self.driver.execute_script("arguments[0].click();", visible_filtered[0])
                    print("✅ First room option selected")
                else:
                    print("⚠️ No visible room options after typing")

            except Exception as type_err:
                print(f"DEBUG: Typing approach failed for rooms: {type_err}")
                print("⚠️ Rooms option not found")

        except Exception as e:
            print("⚠️ Rooms dropdown not found or could not select:", e)

    def selbst_selection(self):
        try:
            person_dropdown = self.wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "ng-select[id*='fuer_wen_wird_die_wohnungsanfrage_gestellt']"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", person_dropdown)

            print(f"DEBUG: Person dropdown found, id: {person_dropdown.get_attribute('id')}")

            # Click the arrow wrapper to open dropdown
            try:
                arrow = person_dropdown.find_element(By.CSS_SELECTOR, ".ng-arrow-wrapper")
                self.driver.execute_script("arguments[0].click();", arrow)
                print("DEBUG: Clicked person arrow wrapper")
            except:
                self.driver.execute_script("arguments[0].click();", person_dropdown)
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
                filtered_options = self.driver.find_elements(By.CSS_SELECTOR, "[role='option'], .ng-option")
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
                    self.driver.execute_script("arguments[0].click();", person_option)
                    print("✅ 'Für mich selbst' selected via typing")
                elif visible_filtered:
                    # If we can't find exact match, try the first option
                    self.driver.execute_script("arguments[0].click();", visible_filtered[0])
                    print("✅ First person option selected")
                else:
                    print("⚠️ No visible person options after typing")

            except Exception as type_err:
                print(f"DEBUG: Typing approach failed for person: {type_err}")
                print("⚠️ Person option not found")

        except Exception as e:
            print("⚠️ Could not select person option:", e)

    def telephone(self, telephone):
        try:
            phone = self.driver.find_element(By.CSS_SELECTOR, "input[id*='telephone_number']")
            phone.clear()
            phone.send_keys(telephone)
            print("✅ Telephone filled")
        except Exception as e:
            print("⚠️ Error filling telephone:", e)

    def privacy(self):
        try:
            checkbox = self.driver.find_element(By.CSS_SELECTOR, "input[id*='datenschutzhinweis']")
            if not checkbox.is_selected():
                checkbox.click()
            print("✅ Datenschutzhinweis clicked")
        except Exception as e:
            print("⚠️ Error clicking Datenschutzhinweis:", e)

    def submit_application(self):
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
                    submit_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
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
                        submit_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
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
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
                time.sleep(0.5)

                # Try multiple click strategies
                click_success = False

                # Strategy 1: JavaScript click
                try:
                    self.driver.execute_script("arguments[0].click();", submit_btn)
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
                            actions = ActionChains(self.driver)
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
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    all_inputs = self.driver.find_elements(By.CSS_SELECTOR,
                                                           "input[type='submit'], input[type='button']")

                    print(
                        f"DEBUG: Found {len(all_buttons)} button elements and {len(all_inputs)} submit/button inputs")

                    for i, btn in enumerate((all_buttons + all_inputs)[:5]):
                        try:
                            btn_id = btn.get_attribute('id') or 'no-id'
                            btn_class = btn.get_attribute('class') or 'no-class'
                            btn_text = btn.text.strip() or btn.get_attribute('value') or 'no-text'
                            print(
                                f"  Button {i}: ID='{btn_id}', Class='{btn_class[:30]}', Text='{btn_text[:30]}'")
                        except:
                            pass
                except:
                    print("DEBUG: Could not enumerate buttons")

        except Exception as e:
            print("⚠️ Error submitting form:", e)


    def gewobag_applying(self, vorname, nachname, email, telephone, date, people, main_window):
        """
        Executes the full Gewobag housing application process with safety checks.
        Returns True if completed successfully, False otherwise.
        """
        try:
            print("🚀 Starting Gewobag application process")

            # 1️⃣ Accept cookies (non-critical)
            self.handle_cookies()

            # 2️⃣ Click 'Anfragen senden' (critical)
            if not self.form_button():
                print("❌ Could not open contact form")
                return False

            # 3️⃣ Switch to iframe (critical)
            if not self.switch_to_iframe(main_window):
                print("❌ Could not switch to iframe — stopping")
                return False

            # 4️⃣ Fill personal info (essential)
            if not self.personal_infos(vorname, nachname, email):
                print("⚠️ Some personal info fields may be missing")

            # 5️⃣ Telephone
            if not self.telephone(telephone):
                print("⚠️ Telephone field failed to fill")

            # 6️⃣ Total people (non-critical)
            self.total_people(people)

            # 7️⃣ WBS selection and date (optional, some listings skip this)
            self.wbs_selection(date)

            # 8️⃣ Room selection
            self.room_selection()

            # 9️⃣ "Für mich selbst" selection
            self.selbst_selection()

            # 🔟 Datenschutzhinweis checkbox (critical)
            if not self.privacy():
                print("❌ Datenschutzhinweis could not be clicked — stopping")
                return False

            # ✅ Submit the form (critical)
            if not self.submit_application():
                print("❌ Could not submit the form")
                return False

            print("✅ Gewobag application completed successfully")
            return True

        except Exception as e:
            print("❌ Fatal error in gewobag_applying:", e)
            return False



