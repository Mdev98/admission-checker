from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
import requests

from mail import send_mail

# Load environment variables
load_dotenv()

# Get email and password from environment variables
EMAIL = os.environ['MAIL']
PASSWORD = os.environ['PASS']

# Set the destination URL
URL = "https://admission.sram.qc.ca/connexion"

# Create a new ChromeDriver instance with the specified options using context manager
with webdriver.Chrome() as driver:
    # Set implicit wait time for the driver to 10 seconds
    driver.implicitly_wait(10)

    # Navigate to the destination page
    driver.get(URL)

    # time.sleep(2)

    # Assert that the page title contains "Admission"
    assert "Admission" in driver.title

    # Find the email and password input fields, and the submit button
    email_box = driver.find_element(By.ID, "courriel")
    password_box = driver.find_element(By.ID, "mot_passe")
    submit_btn = driver.find_element(By.ID, "soumettre_connexion")

    # Fill in the email and password input fields
    email_box.send_keys(EMAIL)
    password_box.send_keys(PASSWORD)

    # Submit the login form
    submit_btn.click()

    # time.sleep(2)
    content = driver.page_source


# Make a soup with the home source page
soup = BeautifulSoup(content, 'html.parser')

# Find the text of the status message,
status = soup.select_one(".texte_statut h3").string.strip()

# Send the status by mail
send_mail(status)