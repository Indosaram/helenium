from selenium_helper import SeleniumLoader

if __name__ == '__main__':
    options = {
        "argument": ["--headless"],
        "experimental_option": {"excludeSwitches": ["enable-logging"]},
    }
    selenium_loader = SeleniumLoader(user_options=options)
