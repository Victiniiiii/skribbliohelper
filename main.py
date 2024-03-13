from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time


def open_skribbl_window():
    skribbl_url = 'https://skribbl.io/'
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(skribbl_url)
    time.sleep(5)
    return driver


def get_skribbl_hints(driver, last_hint):
    hint_elements = driver.find_elements(By.CLASS_NAME, 'hint')  # çizdiğin oyunda da div class = "word"
    hints = []

    if hint_elements:
        for index, hint_element in enumerate(hint_elements):
            hint_text = hint_element.text
            hints.append(hint_text)

    if hints != last_hint:
        result_string = ",".join(hints)
        result_string = result_string.replace(",,", ".")
        result_string = result_string.replace(",", "")
        result_string = result_string.replace(".", " ")
        print("Skribbl.io Hints:", result_string)
        return hints
    else:
        return last_hint


if __name__ == "__main__":
    driver = open_skribbl_window()
    last_hint = []

    while True:
        last_hint = get_skribbl_hints(driver, last_hint)
        time.sleep(2)


