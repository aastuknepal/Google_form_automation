import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Change this at the top of your file
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc-vLBgPj3Abg1lgPJOGJPPOiUkzMbS3yLVS_1j_THzj9g2lQ/viewform?hl=en"

def fill_current_page(driver):
    """Detects and fills any questions on the current screen."""
    # Give the page a moment to finish its sliding animation
    time.sleep(2)
    
    # Find all question blocks on the current page
    radiogroups = driver.find_elements(By.CSS_SELECTOR, 'div[role="radiogroup"]')
    
    for group in radiogroups:
        radios = group.find_elements(By.CSS_SELECTOR, 'div[role="radio"]')
        if not radios:
            continue
            
        # Get the actual values of the options (e.g., "Male", "1", "5")
        data_values = [r.get_attribute("data-value") for r in radios]
        
        # SMART DETECTION: Is this a Likert scale (1-5)?
        if "1" in data_values and "5" in data_values:
            weights = []
            for val in data_values:
                # 40% chance for Option 3, 40% chance for Option 5
                if val =="4":
                    weights.append(80)
                elif val == "3" or val == "5":
                    weights.append(15)
                else:
                    weights.append(2.5) # The remaining options share the rest
            
            chosen_radio = random.choices(radios, weights=weights, k=1)[0]
        
        # Otherwise, it's a standard demographic question (Page 2)
        else:
            # ---> NEW LOGIC: Filter out "Other" <---
            # This creates a new list of options, strictly ignoring any option named "Other"
            valid_radios = [r for r in radios if r.get_attribute("data-value") != "Other"]
            
            # If for some reason the list is empty, default back to all radios, 
            # otherwise pick randomly from the filtered list (Male, Female, etc.)
            if valid_radios:
                chosen_radio = random.choice(valid_radios)
            else:
                chosen_radio = random.choice(radios)
            
        # Scroll to the element and force a click using JavaScript
        try:
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", chosen_radio)
            time.sleep(0.2) 
            driver.execute_script("arguments[0].click();", chosen_radio)
        except Exception as e:
            pass # Ignore layout glitches


def process_form(driver, wait):
    """Navigates through the pages until the form is submitted."""
    while True:
        # 1. Fill any questions on the current page
        fill_current_page(driver)
        
        # 2. Bulletproof Button Hunter
        time.sleep(1) # Brief pause to ensure buttons are interactive
        all_buttons = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
        
        next_btn = None
        submit_btn = None
        
        # Look through all buttons and read their text
        for btn in all_buttons:
            text = btn.text.strip().lower()
            if "next" in text:
                next_btn = btn
            elif "submit" in text:
                submit_btn = btn
                
        if submit_btn and submit_btn.is_displayed():
            # We are on the final page. Click Submit!
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", submit_btn)
            break # Breaks out of the while loop to finish
            
        elif next_btn and next_btn.is_displayed():
            # We are on an intermediate page. Click Next!
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", next_btn)
            
        else:
            print("Error: Could not find 'Next' or 'Submit' text on any button.")
            return False
            
    # 3. Wait for the confirmation page to load (Page 4)
    try:
        # Using 'contains' makes this much more resilient 
        reload_link = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Submit another response")]')))
        
        # Add a slight random delay to mimic human behavior
        time.sleep(random.uniform(1.5, 3.5)) 
        
        # Click "Submit another response" to loop back to Page 1
        driver.execute_script("arguments[0].click();", reload_link)
        return True
    except Exception as e:
        print("Did not reach the confirmation page.")
        return False

from selenium.webdriver.chrome.options import Options # Add this to your imports at the top!

def main():
    print("--- Google Form Auto-Filler ---")
    try:
        num_responses = int(input("How many responses would you like to submit? "))
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        return

    # --- NEW CODE: Force Chrome to English ---
    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--intl.accept_languages=en,en_US")
    
    # Initialize Chrome with the options
    driver = webdriver.Chrome(options=chrome_options)
    # -----------------------------------------
    
    wait = WebDriverWait(driver, 10)

    # Load the form for the very first time
    driver.get(FORM_URL)

    success_count = 0
    for i in range(num_responses):
        print(f"\nSubmitting response {i + 1} of {num_responses}...")
        
        if process_form(driver, wait):
            success_count += 1
            print("-> Success!")
        else:
            print("-> Failed. Stopping script.")
            break 

    print(f"\nDone! Successfully submitted {success_count} out of {num_responses} requested responses.")
    driver.quit()

if __name__ == "__main__":
    main()

