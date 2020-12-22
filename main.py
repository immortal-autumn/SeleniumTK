from src import Visit

file_path = "chromedriver.exe"
web_path = "https://www.bilibili.com/"

# Testing script:
if __name__ == "__main__":
    maj = Visit(file_path, web_path, 10)
    maj.run("study", "晚上好啊~~")
    # maj.exit()