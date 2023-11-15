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

def article_ready(x):
    found = False
    ##AKA_Apr23: Change in Selenium 4.3.0:
    try:
        ##AKA_Feb22: print test
        print(f'try article_ready in ScienceDirectArticlesHandler ... element "body"')
         
        #x.find_element_by_id("body")
        x.finnd_element(by=By.ID, value="body")
        found = True
    except:
        pass
    try:
        #x.find_element_by_id("s0005")
        x.find_element(by=By.ID, value="s0005")
        found = True
    except:
        pass
    return found

class ScienceDirectArticlesHandler():
    def __init__(self, driver):
        self.driver = driver
        self.__logger = logging.getLogger("ScienceDirectArticlesHandler")

    def get_article(self, url):
        url = url.replace("linkinghub.elsevier.com/retrieve/", "sciencedirect.com/science/article/")
        self.__logger.info("Url changed to " + url)
        self.__logger.debug("ScienceDirect::getArticle start " + url)

        result_data = ArticleData(publisher_link=url)

        clear_download_directory()

        self.driver.get(url)
        ##AKA_Feb22: putting a sleep to allow the user to log in.
        ## TODO: create a class to test if user is checked in, direct to log in and pass url before extracting article elements
        time_wait = 30
        print(f'in ScienceDirectArticlesHandler: get_article \n sleeping for {time_wait}s after instance of chromium')
        time.sleep(time_wait)

        ##AKA_Apr23: ERROR/ArticlesDataDownloader 'WebDriver' object has no attribute 'find_element_by_xpath'
        ##AKA_Apr23: assist: https://stackoverflow.com/questions/72754651/attributeerror-webdriver-object-has-no-attribute-find-element-by-xpath
        ## import By | from selenium.webdriver.common.by import By
        ## use driver.find_element(by=By.XPATH, value='//<your xpath>')
        '''
         WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//div[@id='popover-trigger-export-citation-popover']/button/span"))

        export_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element_by_xpath("//div[@id='popover-trigger-export-citation-popover']/button"))
        time.sleep(1)
        export_button.click()


        ris_download_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element_by_xpath("//button[@aria-label='ris']"))
        '''
        ##AKA_Apr23: Change in Selenium 4.3.0: 
        #from selenium.webdriver.common.by import By
        
        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element(by=By.XPATH, value="//div[@id='popover-trigger-export-citation-popover']/button/span"))

        export_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element(by=By.XPATH, value="//div[@id='popover-trigger-export-citation-popover']/button"))
        time.sleep(1)
        export_button.click()

        ris_download_button = WebDriverWait(self.driver, 15).until(
            lambda x: x.find_element(by=By.XPATH, value="//button[@aria-label='ris']"))
        ## End Selenium xpath fix
                
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
            ##AKA_Apr23: xpath fix
            WebDriverWait(self.driver, 15).until(
                lambda x: x.find_element(by=By.XPATH, value="//section[contains(@id, 'sec')]"))
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
