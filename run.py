import sys
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login(id, pw):
    driver = webdriver.Chrome()
    url = "https://knuin.knu.ac.kr/"
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idpw_id")))

    driver.find_element(By.ID, "idpw_id").send_keys(f"{id}")
    driver.find_element(By.ID, "idpw_pw").send_keys(f"{pw}")
    driver.find_element(By.ID, "btn-login").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "mainSnb_title_level2_acc_MNU0010728"))
    )
    time.sleep(2)
    driver.find_element(By.ID, "mainSnb_title_level2_acc_MNU0010728").click()
    time.sleep(2)
    driver.find_element(By.ID, "mainSnb_level3_snbList_button_MNU0010815").click()
    time.sleep(2)
    driver.find_element(By.ID, "mainSnb_level4_snbList_li_MNU0012812").click()

    return driver


def get_today_btn_list(driver):
    TODAY = datetime.today().strftime("%Y-%m-%d")

    time.sleep(3)
    table = driver.find_element(
        By.ID, "tabContentMain_contents_tabPgmMNU0012812_body_grid02_body_tbody"
    )
    rows = table.find_elements(By.TAG_NAME, "tr")

    btn_list = {}
    for r_idx, r_value in enumerate(rows):
        cols = r_value.find_elements(By.TAG_NAME, "td")
        if cols[3].text != TODAY:
            continue
        btn_list[r_idx] = []
        for c_idx, c_value in enumerate(cols):
            if c_idx == 5 or c_idx == 8:
                btn_list[r_idx].append(c_value)
    return btn_list


def get_today_text_list(driver):
    TODAY = datetime.today().strftime("%Y-%m-%d")

    time.sleep(3)
    table = driver.find_element(
        By.ID, "tabContentMain_contents_tabPgmMNU0012812_body_grid02_body_tbody"
    )
    rows = table.find_elements(By.TAG_NAME, "tr")

    text_list = {}
    for r_idx, r_value in enumerate(rows):
        cols = r_value.find_elements(By.TAG_NAME, "td")
        if cols[3].text != TODAY:
            continue
        for c_idx, c_value in enumerate(cols):
            if c_idx == 12:
                text_list[r_idx] = c_value
    return text_list


def add_line(driver):
    TODAY = datetime.today().strftime("%Y-%m-%d")

    time.sleep(3)
    table = driver.find_element(
        By.ID, "tabContentMain_contents_tabPgmMNU0012812_body_grid02_body_tbody"
    )
    rows = table.find_elements(By.TAG_NAME, "tr")

    for r_value in rows:
        cols = r_value.find_elements(By.TAG_NAME, "td")
        if cols[3].text != TODAY:
            continue
        cols[2].find_element(By.TAG_NAME, "input").click()
        break

    driver.find_element(
        By.ID, "tabContentMain_contents_tabPgmMNU0012812_body_udcBtns_btnAdd"
    ).click()


def read_data(txt_path):
    return_dict = {}

    with open(txt_path, "r", encoding="UTF8") as f:
        # login_info = f.readline().strip("\n")
        # return_dict["login"] = login_info.split(" ")

        lines = f.readlines()
        for line in lines:
            line = line.strip("\n").split(" ")
            if line[0] not in return_dict.keys():
                return_dict[line[0]] = {0: [line[1:3], " ".join(line[3:])]}
            else:
                if len(return_dict[line[0]]) == 2:
                    print("error! - too many schedule in a day")
                    return None
                return_dict[line[0]][1] = [line[1:3], " ".join(line[3:])]
    return return_dict


def day_run(TODAY, today_schedule, id, pw):
    for split, click_times in today_schedule.items():
        row_idx = 0 if split == 0 else 0 if len(today_schedule) == 1 else 1
        input_text = click_times[1]
        click_times = click_times[0]
        for idx, click_time in enumerate(click_times):
            print(row_idx, click_time, input_text, end="  ")
            click_time = datetime.strptime(TODAY + " " + click_time, "%Y-%m-%d %H:%M:%S")
            clicked = True
            while clicked:
                TOTIME = datetime.strptime(
                    TODAY + " " + datetime.today().strftime("%H:%M") + ":00", "%Y-%m-%d %H:%M:%S"
                )
                if TOTIME == click_time:
                    driver = login(id, pw)
                    btn_list = get_today_btn_list(driver)
                    txt_list = get_today_text_list(driver)

                    if row_idx == len(btn_list) - 2:
                        row_idx += 1

                    if idx == 1:
                        txt_list[row_idx].find_element(By.TAG_NAME, "input").send_keys(input_text)
                    btn_list[row_idx][idx].click()

                    print("Click!", end="   ")
                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR, "input[title='예']").click()
                    time.sleep(2)
                    driver.quit()
                    clicked = False
                elif TOTIME > click_time:
                    print("Skip!", end="   ")
                    clicked = False
                else:
                    pass
        if split == 0 and len(today_schedule) == 2:
            driver = login(id, pw)
            btn_list = get_today_btn_list(driver)
            if len(btn_list) >= len(today_schedule):
                print("Already!", end="   ")
            else:
                add_line(driver)
                time.sleep(2)
                driver.find_element(By.CSS_SELECTOR, "input[title='확인']").click()
                time.sleep(2)
                print("Add!", end="   ")
            driver.quit()
        print()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Input ID and PW")
        sys.exit()
    else:
        id, pw = sys.argv[1:3]

    data_dict = read_data("data.txt")

    TODAY = datetime.today().strftime("%Y-%m-%d")
    today_schedule = data_dict[TODAY]

    day_run(TODAY, today_schedule, id, pw)
