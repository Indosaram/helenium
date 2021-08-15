import os
import platform
import logging

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class SeleniumLoader:
    def __init__(self, driver_path=None, user_options=None):
        self._get_driver_path()
        if driver_path is None:
            self.driver_path = os.path.join(os.getcwd(), self.driver_filename)
        else:
            self.driver_path = driver_path

        self._init_driver(user_options)
        self._version_checker()

    def _get_driver_path(self):
        current_os = platform.system()

        driver_filename = "chromedriver"
        if current_os == "Linux":
            zip_filename = "chromedriver_linux64.zip"
        elif current_os == "Darwin":
            machine = platform.machine()
            if machine == "x86_64":
                zip_filename = "chromedriver_mac64.zip"
            elif machine == "arm64":
                zip_filename = "chromedriver_mac64_m1.zip"
        elif current_os == "Windows":
            zip_filename = "chromedriver_win32.zip"
            driver_filename = "chromedriver.exe"

        self.zip_filename = zip_filename
        self.driver_filename = driver_filename

    def _init_driver(self, user_options):
        options = webdriver.ChromeOptions()

        if user_options is None:
            options.add_argument("headless")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                "AppleWebKit/537.36 (KHTML, like Gecko)"
                "Chrome/78.0.3904.108 Safari/537.36"
            )
            options.add_argument("lang=ko_KR")
            options.add_argument("log-level=3")
            options.add_experimental_option(
                "excludeSwitches", ["enable-logging"]
            )
        else:
            if "headless" in user_options:
                if user_options["headless"]:
                    options.add_argument("headless")

            if "header" in user_options:
                options.add_argument(user_options["header"])
            else:
                options.add_argument(
                    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                    "Chrome/78.0.3904.108 Safari/537.36"
                )

            if "lang" in user_options:
                options.add_argument(user_options["lang"])
            else:
                options.add_argument("lang=ko_KR")

            options.add_argument("log-level=3")
            options.add_experimental_option(
                "excludeSwitches", ["enable-logging"]
            )
            options.add_argument('w3c=True')
        webdriverpath = os.path.join(self.driver_path)

        try:
            self.driver = webdriver.Chrome(webdriverpath, options=options)
        except WebDriverException:
            logging.warning(
                "No chromedriver executable found. "
                "Download latest version of the driver."
            )
            self._download_chromedriver()
            self.driver = webdriver.Chrome(webdriverpath, options=options)

    def _version_checker(self):
        chrome_version = self.driver.capabilities["browserVersion"][0:4]
        driver_version = self.driver.capabilities["chrome"][
            "chromedriverVersion"
        ].split(" ")[0][0:4]
        if chrome_version != driver_version:
            logging.warning(
                "Chromedriver is outdated."
                "Download latest version of the driver."
            )

            self._download_chromedriver()
            self._init_driver()

    def _download_chromedriver(self):
        import stat
        import zipfile
        import shutil

        import requests

        logging.info("Download chromedriver")
        chromedriver_version_api = (
            "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        )
        response = requests.get(chromedriver_version_api)
        latest_version = response.text

        chromedriver_url = (
            "https://chromedriver.storage.googleapis.com/"
            f"{latest_version}/{self.zip_filename}"
        )
        with requests.get(chromedriver_url, stream=True) as r:
            with open(self.zip_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        with zipfile.ZipFile(self.zip_filename, "r") as file:
            file.extractall(os.getcwd())

        os.chmod(
            self.driver_filename, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )
        os.remove(self.zip_filename)
