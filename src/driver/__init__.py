import time

from selenium import webdriver
from selenium.common import exceptions


# Set up the driver for the browser.
def setup_driver(path, site):
    browser = webdriver.Chrome(executable_path=path)
    browser.maximize_window()
    browser.get(site)
    return browser


def identify(type, driver):
    m_key = {"id": driver.find_element_by_id,
             "class": driver.find_element_by_class_name,
             "name": driver.find_element_by_name,
             "xpath": driver.find_element_by_xpath,
             "default": driver.find_element
             }

    return m_key.get(type)


class Driver:
    def __init__(self, path, site):
        self.path = path
        self.site = site
        self.driver = setup_driver(self.path, self.site)
        # self.handle_tmp = None

    def dir_get(self, page):
        self.driver.get(page)

    def dir_op(self, page):
        script = f"window.open(\"{page}\");"
        self.driver.execute_script(script)

    def sim_click(self, type, key):
        element = identify(type, self.driver)
        try:
            element(key).click()
        except exceptions.NoSuchElementException:
            print(f"{self.driver.title} does not exists click button")

    def sim_input(self, type, key, value):
        try:
            identify(type, self.driver)(key).send_keys(value)
        except exceptions.NoSuchElementException:
            print(f"{self.driver.title} does not exists input area")

    def sim_refresh(self):
        self.driver.refresh()

    def sim_switch(self, ind):
        all_handles = self.driver.window_handles
        self.driver.switch_to.window(all_handles[ind])

    def close_current(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def wait_until_page_changed(self):
        handle_recorded = self.driver.title
        while handle_recorded == self.driver.title:
            pass

    def wupc_rec_cook(self):
        self.wait_until_page_changed()
        return self.driver.get_cookies()

    def inject_cook(self, cookie):
        for s in cookie:
            self.driver.add_cookie(s)

    def record_bilibili_list(self, maximum):
        size = 0
        element = None
        while size < maximum:
            element = self.driver.find_elements_by_css_selector(".room-card-ctnr")
            size = len(element)
            self.scroll_btm()
        return element[:maximum]

    def scroll_btm(self):
        script = "window.scrollTo(0, document.body.scrollHeight);"
        self.driver.execute_script(script)