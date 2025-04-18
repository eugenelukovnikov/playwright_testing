import pytest
import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect

class DashboardPage():
    def __init__ (self, page):
        
        self.page = page

        self.profile_welcome = page.locator("//p[@id='usernameDisplay']")
        self.logout_btn = page.locator("//button[@id='logout']")

    def assert_welcome_message(self, message):
        expect(self.profile_welcome).to_have_text(message)

    def logout(self):

        self.logout_btn.click()