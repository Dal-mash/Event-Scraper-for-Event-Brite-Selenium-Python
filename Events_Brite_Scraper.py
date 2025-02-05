from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv
# Setup Edge WebDriver
service = Service("D:/SOFTWARE/msedgedriver.exe")


driver = webdriver.Edge(service=service)


try:
    driver.get("https://www.eventbrite.com")
    wait = WebDriverWait(driver, 30)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
    time.sleep(5)
    print("Finding events Container...")

    try:
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(5)
        container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.feed-events-bucket__content__cards-container")))
    except Exception as e:
        print(f"Events container not found, skipping... Error: {e}")
        exit()
    finally:
            print("Container found!")

    try:
        elements = container.find_elements(By.CSS_SELECTOR, "section.event-card-details")
    except Exception as e:
        print(f"Event details not found, skipping... Error: {e}")
        exit()
    finally:
        print(f"Found {len(elements)} event")
        global arr
        arr = []
        if(len(elements) == 0):
            print("No events found")
            exit()
        index = 1
        for element in elements:
            try:
                title = element.find_element(By.CSS_SELECTOR, "h3").text.strip()

                link = element.find_element(By.CSS_SELECTOR, "a.event-card-link").get_attribute("href").strip()

                date = element.find_element(By.XPATH, ".//p[contains(text(),'PM') or contains(text(),'AM')]").text.strip()
                
                try:
                    price = element.find_element(By.CSS_SELECTOR, ".DiscoverVerticalEventCard-module__priceWrapper___usWo6").find_element(By.CSS_SELECTOR, "p").text.strip()
                except NoSuchElementException:
                    price = "N/A"


                try:
                    location = element.find_element(By.CSS_SELECTOR, ".event-card__clamp-line--one").text.strip()
                except NoSuchElementException:
                    location = "N/A"



                print(f"{index}: {title}. Date: {date} Location: {location} Price: {price} Link: {link}")
                print("------------------------------------------------------------------")

                ########## Append to array
                arr.append({"Title": title, "Date & Time": date, "Location": location, "Ticket-price": price, "Event-URL": link})

                index+=1
            except Exception as e:
                print(f"{index}: (No title found) Error: {e}")
                
    

finally:
    driver.quit()

print("Data Scraped, Now writing to CSV file...")

with open("events.csv", 'w', newline='', encoding="utf-8") as file:
    fieldnames = ["Title", "Date & Time", "Location", "Ticket-price", "Event-URL"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(arr) 
print("Data written to events.csv")
