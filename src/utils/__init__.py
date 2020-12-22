
def encode_path(cookie_path, path):
    return f"{cookie_path}{path}"



#
# def encode_path(path=cookie_filename):
#     print(f"{cookie_path}{path}")
#     return f"{cookie_path}{path}"
#
#
# def read_cookie(driver):
#     path = encode_path()
#     if os.path.exists(path):
#         cookie = pickle.load(open(path, 'rb'))
#         for c in cookie:
#             if 'expiry' in c:
#                 print(time.time(), c['expiry'])
#                 if c['expiry'] < time.time():
#                     print("Out of dated cookie! Please restart the program!")
#                     os.remove(path)
#                     sys.exit(-3)
#     else:
#         cookie = get_cookie(driver)
#     inject_login(driver, cookie)
#
#
# def save_cookie(cookie):
#     out = open(encode_path(), 'wb')
#     pickle.dump(cookie, out)
#     out.close()
#
#
# def get_cookie(driver):
#     driver.dir_op(login_page)
#     driver.sim_switch(1)
#     cookie = driver.wupc_rec_cook()
#     # print(cookie)
#     save_cookie(cookie)
#     # Bad code, but just exit the program.
#     driver.close_current(driver.driver.quit())
#     return cookie