from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import shutil
import os


def capture_elements(url: str, tmp_dir: str, unit_id: str = "") -> list[str]:
    """Capture all unitCard elements and save images to tmp_dir."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")

    chrome_path = shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium")
    if chrome_path:
        options.binary_location = chrome_path
    else:
        raise RuntimeError("❌ Chrome not found. Please install Google Chrome or Chromium.")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    filenames = []

    try:
        driver.get(url)
        time.sleep(5)

        all_elements = driver.find_elements(By.CSS_SELECTOR, '[id^="unitCard"]')
        elements = [el for el in all_elements if el.get_attribute("id") != "unitCardsContainer"]

        for el in elements:
            el_id = el.get_attribute("id")
            if el_id is not None:
                filename = os.path.join(tmp_dir, f"{unit_id}{el_id.replace('unitCard','')}.png")
                el.screenshot(filename)
                filenames.append(filename)
            else:
                continue

    finally:
        driver.quit()

    return filenames
