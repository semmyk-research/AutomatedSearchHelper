## AKA_Feb22: edit
## //TODO: Selenium methods to be updated - such as find_element_by_id | find_element_by_xpath

## Load libraries
import shutil
import sys
import time
import os

from ArticlesDataDownloader.ScienceDirect.science_direct_html_to_json import science_direct_html_to_json

import re
import logging
## AKA_Feb22: add import By - to fix xpath | #pending
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from ArticlesDataDownloader.ArticleData import ArticleData
from ArticlesDataDownloader.download_pdf_and_prepare_article_data import download_pdf_and_prepare_article_data
from ArticlesDataDownloader.download_utilities import wait_until_all_files_downloaded, wait_for_file_download, \
    clear_download_directory, get_files_from_download_directory, download_pdf, \
    download_file_from_link_that_initiates_download
from ArticlesDataDownloader.ris_to_article_data import ris_to_article_data
##import time

## AKA_Feb22: insert to update depreciated methods
from selenium.webdriver.common.by import By
## AKA_Feb22: utilise selenium exceptions
from selenium.common.exceptions import NoSuchElementException

'''
ScienceDirect: fxn to check class element, to see if user is logged in
'''
def loggedin_ready(x=driver, e_locator):
    found = False
    try:
        ##AKA_Feb22: print test
        print(f'try article_ready in ScienceDirectArticlesHandler ... element "body"')
        ##x.find_element_by_id("body")
        x.find_element(By.CLASS_NAME, e_locator)
        found = True
        print(f' In loggedin_ready, {e_locator} value: {x.find_element(By.CLASS_NAME, e_locator).text}')
    except NoSuchElementException:
        print (f'No Such Element: {e_locator}')
        return False
    except:
        pass
    return found

'''
This fxn takes the sd link, split, and 
return translated link usable post log in.
NB: This fxn might become redundant if a different approached is taken
such as try if user is logged in, if logged in, reuse existing session.
PS: This fxn might still be used in tandem.
'''
def signin_link_url(link):
    txt = link
    ## where link was:     'https://www.sciencedirect.com/search?offset=25&qs=%28%22digital%20technologies%22%20OR%20%22Digital%20technology%22%29%20AND%20%28%22definition%22%20OR%20%22define%22%20OR%20%22coined%22%29&show=100'
    
    ## link url split line (char)
    z = txt.rsplit('?')
    ## Note that z is a list

    ## Note that sciencedirect signin redirect look like     ##https://www.sciencedirect.com/user/login?targetURL=%2Fsearch%3Foffset%3D25%26qs%3D%2528%2522digital%2520technologies%2522%2520OR%2520%2522Digital%2520technology%2522%2529%2520AND%2520%2528%2522definition%2522%2520OR%2520%2522define%2522%2520OR%2520%2522coined%2522%2529%26show%3D100&from=globalheader
    
    signin_prefix = 'https://www.sciencedirect.com/user/login?targetURL=%2Fsearch%3F'
    sd_split = str(z[1]) ##sd link split
    print(f'In signin_link_url, sd_split (z[1]) is: {sd_split}')
    
    ##signin_split_join = ''.join(z[1]) ## currently using str()
    
    ## NB: doesn't work well | signin_url = signin_prefix + signin_split + '&from=globalheader'
    ## Unfortuantely, sciencedirect does not work with the rejoined url.
    ## We need to translate.
    
    ## choice of using chained str.replace or str.translate
    ##Translate make us of maketrans using replacement characters in dict
    ### See https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string
    
    ## AKA_Mar22: sd_split --> signin_split = str(z[1])
    sd_split1 = sd_split.translate(str.maketrans({'%': '%25', '=': '%3D'}))
    ##sd_split1 = signin_split.translate(str.maketrans({'%': '%25', '=': '%3D'}))
    sd_translate_url = signin_prefix + str(sd_split1) + '&from=globalheader'
    print(f'\n SD translated url: {sd_translate_url}')
    
    ##return signin_url
    return sd_translate_url
    
    ## NB: Antivirus mightinterfere with downloaded ris file from SD
    ## NB: SD page might give error
    '''
    This page isn’t working
    www.sciencedirect.com took too long to respond.
    HTTP ERROR 504
    '''

'''
AKA_Feb22: Fxn to check if the user is logged in to sciencedirect.
The print() can safely be commented out. They are for 'debugging purposes.
If the user is not logged in, it waits for time in sec. This being timewait.
'''
'''
AKA_Mar22: //TODO: Perhaps, check_linkpage should only check for log in only.
If not logged in (Hint: catch_isElementPresent), the user should be allowed to log in.
Then we try check_linkpage again, if logged in, we get_driver re-using existing session id
https://tarunlalwani.com/post/reusing-existing-browser-session-selenium/
'''
def check_linkpage(driver, link, output_dir):
    print(f'entering check_linkpage ...')
    ## AKA_Feb22: check if user is logged in to sciencedirect
    sign_status = ''
    sign_string = 'Sign in'
    sign_ID = 'link-button-text'
    signout_ID = 'button-link-text'
    driver.get(link)        
    print(f'In check_linkpage: Checking for "{sign_string}" in sign_ID="{sign_ID}"')
    ##AKA_Mar22: Moved to while loop
    ##catch_isElementPresent(driver, sign_ID)
    '''
        Note the inspect element from sciencedirect webpage.
        <a class="link-button u-margin-m-left link-button-primary link-button-small" role="button" href="/user/login?targetURL=%2Fsearch%3Foffset%3D25%26qs%3D%2528%2522digital%2520technologies%2522%2520OR%2520%2522Digital%2520technology%2522%2529%2520AND%2520%2528%2522definition%2522%2520OR%2520%2522define%2522%2520OR%2520%2522coined%2522%2529%26show%3D100&amp;from=globalheader" id="gh-signin-btn" data-aa-region="header" data-aa-name="Sign in">
        <span class="link-button-text">Sign in</span></a>
    '''
    ## Beware 'link-button-text' may return 'Sign in' or 'Register'
    
    '''
    ## AKA_Mar22: 
    '''
    catch_isElementPresent(driver, sign_ID)
    while True:
        ##catch_isElementPresent:
        ##catch_isElementPresent(driver, sign_ID)
        if catch_isElementPresent.e_locator_text == 'Sign in' or 'Register':
            ##delay calling page directly. Allow for signing in
            signin_link = signin_link_url(link)
            ## change link to new link
            driver.get(signin_link)
        
            print(f'In check_linkpage, pausing while True')
            timewait = 40
            time.sleep(timewait)
            
            if isElementPresent(driver, signout_ID):
                print(f'breaking out of while "if" loop: signout_ID - button-link-text')
                break
            catch_isElementPresent(driver, sign_ID)

    print(f'In check_linkpage, going to download_acm_citations_from_search_link')
    ##AKA_Mar22: Perhaps, moved to Main
    ##download_acm_citations_from_search_link(driver, link, output_dir)
            ##TODO: perhaps reuse existing session id
    return
        


'''
## AKA_Feb22: function to find element on a page loaded by selenium webdriver
## See https://stackoverflow.com/questions/65212611/check-if-element-exists-selenium-python
'''
def isElementPresent(driver, e_locator):
    try:
        driver.find_element(By.CLASS_NAME, e_locator)
    except NoSuchElementException:
        print (f'No Such Element: {e_locator}')
        return False
    return True

def catch_isElementPresent(driver, e_locator):
    print(f'entering catch_isElementPresent | driver is {driver} | element is {e_locator}')
    try:
        if isElementPresent(driver, e_locator):
            catch_isElementPresent.e_locator_text = driver.find_element(By.CLASS_NAME, e_locator).text
            print(f' In catch_isElementPresent, {e_locator} value: {catch_isElementPresent.e_locator_text}')
            ##break

        ##time.sleep(5)
    except NoSuchElementException as e:
        print(f'Timeout getting element {e_locator}, Description: {repr(e)}')
        
    ##time.sleep(5)
    return 


class ScienceDirectArticlesCheckurl():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ScienceDirectArticlesCheckurl")

    def get_article(self, url):
        url = url.replace("linkinghub.elsevier.com/retrieve/", "sciencedirect.com/science/article/")
        self.__logger.info("Url changed to " + url)
        self.__logger.debug("ScienceDirect::getArticle start " + url)

        result_data = ArticleData(publisher_link=url)

        clear_download_directory()

        self.driver.get(url)
        '''
        ##AKA_Mar22: try using while True:
        ##AKA_Feb22: putting a sleep to allow the user to log in.
        ## TODO: create a class to test if user is checked in, direct to log in and pass url before extracting article elements
        time_wait = 30
        print(f'in ScienceDirectArticlesHandler: get_article \n sleeping for {time_wait}s after instance of chromium')
        time.sleep(time_wait)
        '''

        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@id='popover-trigger-export-citation-popover']/button/span"))

        export_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element_by_xpath("//div[@id='popover-trigger-export-citation-popover']/button"))
        time.sleep(1)
        export_button.click()


        ris_download_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element_by_xpath("//button[@aria-label='ris']"))

        ris_download_button.click()
        time.sleep(1) # wait until download initiated
        wait_until_all_files_downloaded(self.driver)
        downloaded_files = get_files_from_download_directory()

        if len(downloaded_files) == 1:
            self.__logger.debug('File downloaded successfully - reading data')
            result_data.merge(ris_to_article_data(downloaded_files[0]))
            clear_download_directory()

        try:
            self.driver.get(url)
            self.__logger.debug("Called get for  " + url)
            WebDriverWait(self.driver, 15).until(
                lambda x: x.find_element_by_xpath("//section[contains(@id, 'sec')]"))
            result_data.merge(ArticleData(text=science_direct_html_to_json(self.driver.page_source)))
            result_data.read_status = 'OK'
        except Exception as error:
            self.__logger.error(str(error))
            self.__logger.error("Could not read html text for " + url)

        return result_data


    def download_pdf(self, url):
        id = re.findall("/pii/(.*?)/", url + '/')[0]
        pdf_link = 'https://www.sciencedirect.com/science/article/pii/%s/pdfft?isDTMRedir=true&download=true' % id
        self.__logger.info('Trying to get pdf from ' + pdf_link)
        return download_file_from_link_that_initiates_download(self.driver, pdf_link)

    def is_applicable(self, url):
        for link_part in ['linkinghub.elsevier.com', 'sciencedirect.com']:
            if link_part in url:
                return True
        return False


    def name(self):
        return "ScienceDirect"
