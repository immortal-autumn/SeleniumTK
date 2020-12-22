# A visitor for BILIBILI client -> which is used for sending greeting messages to livers.
import os
import pickle
import sys
import time

from src.driver import Driver

login_page = "https://passport.bilibili.com/login"

cookie_path = "cookies/"

cookie_filename = "bilibili"


def encode_path(path=cookie_filename):
    print(f"{cookie_path}{path}")
    return f"{cookie_path}{path}"


def read_cookie(driver):
    path = encode_path()
    if os.path.exists(path):
        cookie = pickle.load(open(path, 'rb'))
        for c in cookie:
            if 'expiry' in c:
                print(time.time(), c['expiry'])
                if c['expiry'] < time.time():
                    print("Out of dated cookie! Please restart the program!")
                    os.remove(path)
                    sys.exit(-3)
    else:
        cookie = get_cookie(driver)
    inject_login(driver, cookie)


def save_cookie(cookie):
    out = open(encode_path(), 'wb')
    pickle.dump(cookie, out)
    out.close()


def get_cookie(driver):
    driver.dir_op(login_page)
    driver.sim_switch(1)
    cookie = driver.wupc_rec_cook()
    # print(cookie)
    save_cookie(cookie)
    # Bad code, but just exit the program.
    driver.close_current(driver.driver.quit())
    return cookie


def inject_login(driver, cookie):
    driver.inject_cook(cookie)
    driver.sim_refresh()


def automatic_in(driver, i, message):
    driver.sim_switch(i)
    driver.sim_input("class", "chat-input", message)
    driver.sim_click("class", "bl-button")
    driver.close_current()


def automatic_running(driver, area, maximum, message):
    m_area = {
        "study": "https://live.bilibili.com/p/eden/area-tags?parentAreaId=11&areaId=0",
        "entertainment": "https://live.bilibili.com/p/eden/area-tags?parentAreaId=1&areaId=0",
        "vb": "https://live.bilibili.com/p/eden/area-tags?parentAreaId=9&areaId=0"
    }
    link = m_area.get(area)
    driver.dir_get(link)
    r_list = driver.record_bilibili_list(maximum)
    # High performance text entry
    # for r in r_list[35:40]:
    #     r.click()
    #     driver.sim_switch(1)
    #     driver.sim_input("class", "chat-input", message)
    #     driver.sim_click("class", "bl-button")
    #     driver.close_current()
    #     time.sleep(0.05)

    size = len(r_list)
    si = size % 5
    re = int(size / 5)
    for r in range(re):
        for i in range(5):
            r_list[r * 5 + i].click()
        time.sleep(0.5)
        for i in range(5):
            automatic_in(driver, 1, message)

    for r in r_list[size - si: size]:
        r.click()
        automatic_in(driver, 1, message)
        time.sleep(0.05)


# Class that leads with thread-safe operation
class Visit:
    def __init__(self, file_path, web_path, maximum):
        self.driver = Driver(file_path, web_path)
        self.maximum = maximum

    def run(self, area, msg):
        driver = self.driver
        read_cookie(driver)
        automatic_running(driver, area, self.maximum, msg)

    def exit(self):
        time.sleep(5)
        self.driver.driver.quit()
