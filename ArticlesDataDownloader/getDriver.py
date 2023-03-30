## AKA_Feb22 edit

import os

from selenium import webdriver
## AKA_Mar22:
from webdriver_manager.chrome import ChromeDriverManager

from ArticlesDataDownloader.download_utilities import clear_download_directory, DOWNLOAD_DIRECTORY

## AKA_Feb22: pass arg proxyFile as optional
def getDriver(proxyFile=None):
    chrome_options = webdriver.ChromeOptions()
    if proxyFile:
        pluginfile = proxyFile
        chrome_options.add_extension(pluginfile)

    clear_download_directory()

    preferences = {
                   "download.default_directory": DOWNLOAD_DIRECTORY,
                   "directory_upgrade": True,
                   "plugins.always_open_pdf_externally": True,
                   "safebrowsing.enabled": True}

    chrome_options.add_experimental_option("prefs", preferences)
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--kiosk")

    ## AKA_Feb22: added to test chromedriver path
    ## We can do away with path by simply adding chromedriver to Python Scripts folder
    '''
    selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see https://chromedriver.chromium.org/home
    --------- 
    https://stackoverflow.com/questions/29858752/error-message-chromedriver-executable-needs-to-be-available-in-the-path
    done automatically using webdriver-manager

    pip install webdriver-manager
    Now the above code in the question will work simply with below change,

    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(ChromeDriverManager().install())
    '''
    ##driver = webdriver.Chrome('C:\Dat\Anaconda3\Lib\site-packages\selenium\webdriver\chromium')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        options=chrome_options)
    driver.refresh()

    return driver


'''
AKA_Feb22: Side note
connect / inspect existing Chrome session
Note: admx.help 

Read:
https://tarunlalwani.com/post/reusing-existing-browser-session-selenium/
https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session 
https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/
'''

'''
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

# executor_url = driver.command_executor._url
# session_id = driver.session_id

def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)
    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver

bro = attach_to_session('http://127.0.0.1:64092', '8de24f3bfbec01ba0d82a7946df1d1c3')
bro.get('http://ya.ru/')
'''