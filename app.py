from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import time
import logging

website_queries = 100
domain = "http://127.0.0.1:5000/"

logging.basicConfig(filename='./app.log', level=logging.INFO, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

if not os.path.exists("screenshots"):
    os.makedirs("screenshots/pass")
    os.makedirs("screenshots/fail")

data = pd.read_csv("./assets/top-1m.csv", names=["rank", "domain"])

queries = [x for x in data['domain'].sample(website_queries)]

binary = "./geckodriver"
driver = webdriver.Firefox(executable_path=binary)
driver.set_window_size(1366, 768)

logging.info("Test webpage {}".format(domain))

for query in queries:
    driver.get(domain)

    try:
        # Wait until the `input` element appear on home page (up to 15 seconds)
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.TAG_NAME, "input"))
        )
        try:
            # Clear the input area and add the query
            driver.find_element_by_tag_name("input").clear()
            driver.find_element_by_tag_name('input').send_keys(query)

            try:
                # Wait until the `loading_btn` element appear (up to 15 seconds)
                WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, 'loading_btn'))
                )

                # Click the `loading_btn` element to get results
                driver.find_element_by_id('loading_btn').click()

                try:
                    # Wait until the `result` element with data on domain appear (up to 20 seconds)
                    WebDriverWait(driver, 20).until(
                        EC.visibility_of_element_located((By.TAG_NAME, "h2"))
                    )

                    # Wait for charts and images to be drawn
                    time.sleep(2)

                    result_heading = driver.find_element_by_tag_name("h2").text

                    if "This is what we found about" in result_heading:
                        logging.info("{0} Data found. See screenshots/pass/{0}.png".format(query))
                    else:
                        logging.info("{0} Data not found. See screenshots/pass/{0}.png".format(query))

                    # Make screenshot
                    page_html = driver.find_element_by_tag_name('html')
                    page_html.screenshot("screenshots/pass/{}.png".format(query))

                except:
                    logging.error("{0} error Connection dropped. Took more time than expected. See screenshots/fail/failed_{0}.png".format(query))

                    page_html = driver.find_element_by_tag_name('html')
                    page_html.screenshot("screenshots/fail/failed_drop_connection_{}.png".format(query))

            except:
                logging.error("{0} error Cannot click the button. See screenshots/fail/failed_click_{0}.png".format(query))

                page_html = driver.find_element_by_tag_name('html')
                page_html.screenshot("screenshots/fail/failed_click_{}.png".format(query))

        except:
            logging.error("{0} error cannot submit the form. See screenshots/fail/failed_form_{0}.png".format(query))

            page_html = driver.find_element_by_tag_name('html')
            page_html.screenshot("screenshots/fail/failed_form_{}.png".format(query))

    except:
        logging.error("{0} error cannot connect to {1}. See screenshots/fail/failed_connection_{0}.png".format(query, domain))

        page_html = driver.find_element_by_tag_name('html')
        page_html.screenshot("screenshots/fail/failed_connection_{}.png".format(query))

driver.close()
