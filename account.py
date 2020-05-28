from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time

# Hashes for instagrams graphql api queries
graphql_followers_hash = "37479f2b8209594dde7facb0d904896a"
graphql_followings_hash = "58712303d941c6855d4e888c5f0cd22f"
graphql_api_template = 'https://www.instagram.com/graphql/query/?query_hash={}&variables={{"id":"{}",' \
                       '"first":100,"after":"{}"}}'

api_account_info = "https://www.instagram.com/{}/?__a=1"

xpath_login_submit = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button'


class Account:
    # Create a Selenium driver, log in, and get own profile id
    def __init__(self, username, password):
        self.username = username

        # Setting up webdriver
        self.driver = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application/Chromedriver.exe")

        # Login to Instagram session, passing pw as argument so the class doesn't store it
        self.login_to_instagram(password)

        # Opening api website of account
        self.driver.get(api_account_info.format(self.username))

        # Parse api response to json
        site_soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        self.profile_data_json = json.loads(site_soup.find("body").text)

        self.id = self.profile_data_json["graphql"]["user"]["id"]

        self.follower_list = []

    def login_to_instagram(self, password):
        self.driver.get("https://www.instagram.com/accounts/login")

        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_xpath(xpath_login_submit).click()

        time.sleep(2)

    # returns a list of all the accounts that follow you
    def get_followers(self):
        # if the followers were already queried, return them from self
        if self.follower_list:
            return self.follower_list

        has_next_page = True
        next_page_cursor = ""

        while has_next_page:
            # query the next page of accounts
            self.driver.get(graphql_api_template.format(graphql_followers_hash, self.id, next_page_cursor))
            site_soup = BeautifulSoup(self.driver.page_source, features="html.parser")
            response_followers_json = json.loads(site_soup.find("body").text)

            # if there is no next page, don't iterate anymore
            if not response_followers_json["data"]["user"]["edge_followed_by"]["page_info"]["has_next_page"]:
                has_next_page = False

            next_page_cursor = response_followers_json["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]

            # add the following accounts to the follower-list
            for follower in response_followers_json["data"]["user"]["edge_followed_by"]["edges"]:
                self.follower_list.append(follower["node"]["username"])

        return self.follower_list

    def query_biography(self, account_name):
        self.driver.get(api_account_info.format(account_name))
        site_soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        account_info_json = json.loads(site_soup.find("body").text)
        return account_info_json["graphql"]["user"]["biography"]

    # close the selenium window
    def close(self):
        self.driver.close()
