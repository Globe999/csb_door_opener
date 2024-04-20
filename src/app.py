import os
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller
import time
from dotenv import load_dotenv
from waitress import serve

app = Flask(__name__)

load_dotenv()
chromedriver_autoinstaller.install()

BASE_URL = os.environ.get("BASE_URL")
LINK_URL = os.environ.get("LINK_URL")
APTUS_URL = os.environ.get("APTUS_URL")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
ENTRANCE_DOOR_ID = os.environ.get("ENTRANCE_DOOR_ID")
PORT = os.environ.get("PORT")

@app.route('/open', methods=['GET'])
def open_door():

    if request.args.get('api_key') != os.environ.get('API_KEY'):
        return "Unauthorized", 401

    print("Here")
    driver = webdriver.Chrome(options=set_chrome_options())
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(2)

    driver.get(BASE_URL)

    title = driver.title
    driver.find_element(By.ID, "user_login").send_keys(USERNAME)
    driver.find_element(By.ID, "user_pass").send_keys(PASSWORD)
    driver.find_element(By.XPATH, '//button[text()="Logga in"]').click()

    wait.until(EC.url_changes(BASE_URL), "Login failed")

    link = driver.find_element(By.XPATH,f'//a[contains(@href,"{LINK_URL}")]').get_attribute("href")

    driver.get(link)
    # Wait for the page to load
    wait.until(EC.url_to_be(APTUS_URL))

    door = driver.find_element(By.ID, ENTRANCE_DOOR_ID)
    if door:
        door.click()
        result = {"status": "success", "message": "Door opened successfully"}
    else:
        result = {"status": "failure", "message": "Door not found"}, 400

    time.sleep(3)
    driver.close()

    return jsonify(result)

def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


if __name__ == '__main__':
    if os.environ.get("ENV") == "development":
        app.run(debug=True, host="0.0.0.0", port=int(PORT))
    else:
        serve(app, host="0.0.0.0", port=int(PORT))