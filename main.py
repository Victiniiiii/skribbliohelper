from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

font_size = "20px"
font_size2 = "40px"
font_color = "white"
final_words = ""
last_printed_hints = ""
last_printed_word_lengths = ""
closest_words = []
word_dataset = []
with open("output.txt", "r") as file:
    for line in file:
        word, _ = line.strip().split(',', 1)
        word_dataset.append(word)


def open_skribbl_window():
    skribbl_url = 'https://skribbl.io/'
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    driver.get(skribbl_url)
    time.sleep(5)
    return driver


def get_skribbl_hints(driver):
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


def suggest_closest_words(current_word, word_dataset):
    filtered_words = [word for word in word_dataset if len(word) == len(current_word)]
    possible_words = []

    for word in filtered_words:
        match = True
        for char1, char2 in zip(current_word, word):
            if char1 != '_' and char1 != char2:
                match = False
                break
        if match:
            possible_words.append(word)
    return possible_words


def print_stuff(hints, word_lengths, result_string, word_dataset):
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
                    print(final_words, "already in database")
            final_words = ""

        elif hints and word_lengths != "":
            print("Skribbl.io Hints:", result_string, "Word Length:", word_lengths)
            closest_words = suggest_closest_words(result_string, word_dataset)
            if len(closest_words) > 20:
                print("Possible Word Count:", len(closest_words))
                console_output = f'Possible Word Count: {len(closest_words)}'
                script = f'document.querySelector(".ad-1").style.fontSize = "{font_size2}";'
                script += f'document.querySelector(".ad-1").style.color = "{font_color}";'
                script += f'document.querySelector(".ad-1").innerText = `{console_output}\\n`;'
                driver.execute_script(script)
            else:
                print("Possible Words:", ", ".join(closest_words))
                console_output = f'Possible Words: {", ".join(closest_words)}'
                script = f'document.querySelector(".ad-1").style.fontSize = "{font_size}";'
                script += f'document.querySelector(".ad-1").style.color = "{font_color}";'
                script += f'document.querySelector(".ad-1").innerText = `{console_output}\\n`;'
                driver.execute_script(script)

        last_printed_hints = hints
        last_printed_word_lengths = word_lengths


if __name__ == "__main__":
    driver = open_skribbl_window()
    while True:
        hints, result_string = get_skribbl_hints(driver)
        word_lengths = get_word_lengths(driver)
        print_stuff(hints, word_lengths, result_string, word_dataset)
        time.sleep(1)
