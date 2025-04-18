import pytest
import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

class LoginPage():
    def __init__ (self, page):
        
        self.page = page

        self.username_input = page.locator("//input[@id='username']")
        self.password_input = page.locator("//input[@id='password']")
        self.login_button = page.locator("//button[@id='login']")
        self.error_msg = page.locator("//div[@id='errorAlert']")
        self.expected_error_msg = 'Invalid credentials. Please try again.'

    def open_page(self):
        
        self.page.goto('https://zimaev.github.io/pom/')
    
    def login(self, username, password):

        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message(self):
   
        return self.error_msg.inner_text()

