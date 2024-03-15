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
    hint_elements = driver.find_elements(By.CLASS_NAME, 'hint')
    hints = []

    if hint_elements:
        for hint_element in hint_elements:
            hint_text = hint_element.text
            hints.append(hint_text)

    result_string = ",".join(hints)
    result_string = result_string.replace(",,", ".")
    result_string = result_string.replace(",", "")
    result_string = result_string.replace(".", " ")

    return hints, result_string


def get_word_lengths(driver):
    word_length_elements = driver.find_elements(By.CLASS_NAME, 'word-length')
    word_lengths = ""

    for word_length_element in word_length_elements:
        word_length = word_length_element.text
        word_lengths += word_length + " "

    return word_lengths.strip()


final_words = ""
last_printed_hints = ""
last_printed_word_lengths = ""

def print_stuff(hints, word_lengths, result_string):
    global final_words, last_printed_hints, last_printed_word_lengths

    if hints != last_printed_hints or word_lengths != last_printed_word_lengths and word_lengths != '':

        if "_" not in result_string and not result_string.isspace():
            final_words = result_string

        if final_words and word_lengths != "":
            string_to_write = final_words + "," + word_lengths + "," + "\n"
            with open("output.txt", "r") as file:
                if string_to_write not in file.read():
                    print("Added", final_words, "to the database.")
                    with open("output.txt", "a") as file:
                        file.write(string_to_write)
                else:
                    print("Word already in database")
            final_words = ""

        elif hints and word_lengths != "":
            print("Skribbl.io Hints:", result_string, "Word Length:", word_lengths)

        last_printed_hints = hints
        last_printed_word_lengths = word_lengths


if __name__ == "__main__":
    driver = open_skribbl_window()
    last_hint = []

    while True:
        last_hint, result_string = get_skribbl_hints(driver, last_hint)
        word_lengths = get_word_lengths(driver)
        print_stuff(last_hint, word_lengths, result_string)
        time.sleep(2)
