#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import os

USERNAME = "XXX@gmail.com"
PASSWORD = "SECRET"
SAVE_FILE = "link_list.txt"
COMPANY = "https://www.linkedin.com/company/Microsoft/"

def get_employees(page):
    #usrs = document.querySelectorAll("div.ph0 > ul > li")
    user_list_block = page.query_selector_all("div.ph0 > ul > li")
    answ=os.path.exists(SAVE_FILE)
    opened_file = open(SAVE_FILE, "a" if answ else "w")

    #print(user_list_block)
    for usr in user_list_block:
        #u.querySelector('span[aria-hidden]').innerHTML
        try:
            user = usr.query_selector_all("span[aria-hidden]")[0].inner_text()
            opened_file.write(user)
            opened_file.write("\n")
        except Exception as e:
            pass
        else:
            print(user)
    opened_file.close()

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    # Open new page
    page = context.new_page()
    # Go to https://www.linkedin.com/
    page.goto("https://www.linkedin.com/")
    # Click [placeholder=" "]
    page.click("[placeholder=\" \"]")
    # Fill [placeholder=" "]
    page.fill("[placeholder=\" \"]", USERNAME)
    # Click text=Password Show >> [placeholder=" "]
    page.click("text=Password Show >> [placeholder=\" \"]")
    # Fill text=Password Show >> [placeholder=" "]
    page.fill("text=Password Show >> [placeholder=\" \"]", PASSWORD)
    # Click button:has-text("Sign in")
    # with page.expect_navigation(url="https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"):
    with page.expect_navigation():
        page.click("button:has-text(\"Sign in\")")
    # assert page.url == "https://www.linkedin.com/feed/?trk=homepage-basic_signin-form_submit"

    page.goto(COMPANY)
    with page.expect_navigation():
        page.click("span:has-text(\"employees\")")

    a = 0
    while(a <= 100):
        get_employees(page)
        for i in range(1000):
            page.keyboard.press("ArrowDown")
        page.mouse.click(0,0)
        with page.expect_navigation():
            page.click("[aria-label=\"Next\"]")
        a+= 1
    
    # Logout
    # Click #ember33
    page.click("#ember33")
    # Click text=Sign Out
    # with page.expect_navigation(url="https://www.linkedin.com/home"):
    with page.expect_navigation():
        page.click("text=Sign Out")
    # ---------------------

    #CLose
    page.close()
    #browser.close()


with sync_playwright() as playwright:
    run(playwright)