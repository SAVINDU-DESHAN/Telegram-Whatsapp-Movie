from telethon import TelegramClient, sync, events
from telethon.tl.types import InputPeerChannel
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Input your API details here
api_id = ''  # API ID
api_hash = ''  # API HASH
phone_number = ''  # Phone number

# This part of the code handles opening of WhatsApp on a new Chrome Window
print("NOTE: Please do not alter anything on the opened Chrome window except scanning the QR code")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)  # Increased the wait time

target = ''  # The name of the targeted group on WhatsApp

with TelegramClient('Comet01', api_id, api_hash) as client:
    print("This program just started! All new posts would be sent to " + target)

    @client.on(events.NewMessage(incoming=True))  # For every new message posted to the Telegram channel
    async def my_event_handler(event):
        msg = event.message.message
        print(msg)  # Print the message to the console

        # Switch to the WhatsApp Chrome window
        driver.switch_to.window(driver.window_handles[-1])

        # Wait for the QR code to appear
        try:
            qr_code_element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/div[2]/div[1]/div/div[2]/div/canvas')))
            # Perform actions with the QR code element
        except TimeoutException:
            print("Timed out waiting for the QR code to appear")
            return
        
        # Find the input box and send the message
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]')))
        message_box.send_keys(msg)
        message_box.send_keys(Keys.ENTER)

        # Switch back to the Telegram Chrome window
        driver.switch_to.window(driver.window_handles[0])

    # Run the Telethon client
    client.start()
    client.run_until_disconnected()