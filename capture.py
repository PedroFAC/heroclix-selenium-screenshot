from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import shutil
import os
import time


def capture_elements(url: str, tmp_dir: str, unit_id: str = "") -> list[str]:
    """Capture all unitCard elements and save images to tmp_dir."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    chrome_path = shutil.which("chromium") or shutil.which("google-chrome") or shutil.which("chrome")
    if chrome_path:
        options.binary_location = chrome_path
    else:
        raise RuntimeError("❌ Chrome not found. Please install Google Chrome or Chromium.")

    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),  # use system driver
        options=options
    )

    filenames = []
    try:
        driver.get(url)
        time.sleep(5)

        all_elements = driver.find_elements(By.CSS_SELECTOR, '[id^="unitCard"]')
        elements = [el for el in all_elements if el.get_attribute("id") != "unitCardsContainer"]

        for el in elements:
            el_id = el.get_attribute("id")
            if el_id:
                filename = os.path.join(tmp_dir, f"{unit_id}{el_id.replace('unitCard','')}.png")
                el.screenshot(filename)
                filenames.append(filename)
    finally:
        driver.quit()

    return filenames
