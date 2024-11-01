# Usage example
from scrape_sporty.config import edge_driver_generator
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
import time
import pandas as pd

data = []


with edge_driver_generator() as driver:
    driver.get("https://www.sportybet.com/ng/virtual/")

    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    try:
        # Wait until the element is visible
        link = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Football League']"))
        )
        link.click()
        search_link = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//li[@id='game_league_results-history']/a")
            )
        )
        search_link.click()

        menu_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.XPATH,
                    "//div[@class='menu']/div[@class='item ng-star-inserted' or @class='item selected ng-star-inserted']",
                )
            )
        )
        for item in menu_items:
            item.click()

            time.sleep(10)

            while True:
                try:
                    # Wait until the button is clickable, then get the reference to it
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (
                                By.XPATH,
                                "//button[@class='btn-load-more-tickets btn btn-lg btn-block ng-star-inserted']",
                            )
                        )
                    )
                    button.click()
                    print("Button clicked successfully.")

                    # Optional: wait briefly between clicks to avoid overwhelming the page
                    time.sleep(1)

                except (ElementClickInterceptedException, NoSuchElementException):
                    print("Button is no longer clickable or no longer available.")
                    break
                except Exception as e:
                    print("An error occurred:", e)
                    break
                
            # Retrieve all match containers
            containers = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, ".history-container")
                )
            )

            for container in containers:
                game = container.find_element(
                    By.CSS_SELECTOR, ".event-block-game"
                ).text.removesuffix(":")
                league = container.find_element(By.CSS_SELECTOR, ".event-block-name").text
                league_week = container.find_element(
                    By.CSS_SELECTOR, ".event-block-id"
                ).text
                date = container.find_element(By.CSS_SELECTOR, ".event-block-date").text

                matches = container.find_elements(By.CSS_SELECTOR, ".football-event-block")

                for match in matches:
                    try:
                        event_id = match.find_element(By.CSS_SELECTOR, ".event-id").text
                        team_a_name = match.find_element(
                            By.CSS_SELECTOR, ".teamA .participant-text-name"
                        ).text
                        score = match.find_element(
                            By.CSS_SELECTOR, ".match-result-score"
                        ).text
                        team_b_name = match.find_element(
                            By.CSS_SELECTOR, ".teamB .participant-text-name"
                        ).text

                        # Append the match details as a dictionary to the data list
                        data.append(
                            {
                                "Game": game,
                                "League": league,
                                "League_Week": league_week,
                                "Event ID": event_id,
                                "Date": date,
                                "Team A": team_a_name,
                                "Score": score,
                                "Team B": team_b_name,
                            }
                        )
                    except Exception as e:
                        print(f"Error extracting data for one match: {e}")
            
            time.sleep(2)
    except Exception as e:
        print("Link not found or another error occurred:", e)

df = pd.DataFrame(data)
df.to_csv("match_data.csv", index=False)

# Display the DataFrame
print(df)
