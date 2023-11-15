## AKA_Feb22 edit
## download_science_direct_citations_from_search_link.py
## This return a search of the keywords and download .ris file.
## It does not download fulltext pdf files.
## TODO: ArticlesDataDownloader.readArticle | read_article

import os
import shutil
import sys
import time

from selenium.webdriver.support.wait import WebDriverWait
## AKA_Feb22: insert to update depreciated methods
from selenium.webdriver.common.by import By

from ArticlesDataDownloader.download_utilities import download_file_from_click_of_button
from ArticlesDataDownloader.getDriver import getDriver
## getDriver.py is located inside the ArticlesDataDownloader folder
## AKA_Feb22: utilise helper fxns
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
## AKA_Feb22: utilise selenium exceptions
from selenium.common.exceptions import NoSuchElementException


def download_acm_citations_from_search_link(driver, link, output_directory):
    ## AKA_Feb22 | print msgs for 'debugging' purposes
    print(f'entering download_..._search_Link')
    ##AKA_Feb22: temporary disable. to move to check_linkpage function
    driver.get(link)
    print(f'download_..._search_Link: got link')
    ##AKA_Feb22 time.sleep(3)
    ##AKA_Feb22 ##wait for 2mins. Should allow for log in.
    time.sleep(10) ##120
    ##AKA_Feb22 MAX_PAGES = 50
    MAX_PAGES = 2000
    print(f'download_..._search_Link: to wait per time_wait')
    time_wait = 9
    print(f'download_..._search_Link: waiting {time_wait}')
    
    ## AKA_Feb22: 
    for page_no in range(1, MAX_PAGES + 1):
        output_filename = os.path.join(output_directory, 'science_direct_auto_' + str(page_no) + '.ris')
        print(f'\n download_..._search_Link: output file is {output_filename}')
        print(f'download_..._search_Link: driver is {str(driver)}')
        
        time.sleep(9)  ##(9)
        
        '''
        select_all_checkbox = WebDriverWait(driver, time_wait).until(
            lambda x: x.find_element_by_xpath("//label[@for='select-all-results']/span"))
        '''
        ##AKA_Apr23: Change in Selenium 4.3.0: 
        select_all_checkbox = WebDriverWait(driver, time_wait).until(
            lambda x: x.find_element(By.XPATH, "//label[@for='select-all-results']/span"))
        print(f'downloadSDcitation4mSearchLink_..._search_Link: selecting all checkbox')
        
        ## Refer bottom for XPATH
        
        desired_y = (select_all_checkbox.size['height'] / 2) + select_all_checkbox.location['y']
        print(f'download_..._search_Link: desired_y is {str(desired_y)}')
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

        ##print(f'download_..._search_Link: about to select {str(select_all_checkbox.click().text)}')
        select_all_checkbox.click()
        ##print(f'download_.._search_Link: selected {str(select_all_checkbox.click().value)}')

        '''
        export_button = WebDriverWait(driver, time_wait).until(
            lambda x: x.find_element_by_xpath("//span[@class='export-all-link-text']"))
        export_button.click()
        '''
        ##AKA_Apr23: Change in Selenium 4.3.0: 
        export_button = WebDriverWait(driver, time_wait).until(
            lambda x: x.find_element(By.XPATH, "//span[@class='export-all-link-text']"))
        export_button.click()

        '''
        ris_button = WebDriverWait(driver, time_wait).until(
            lambda x: x.find_element_by_xpath("//span[contains(text(),'Export citation to RIS')]"))
        '''
        ris_button = WebDriverWait(driver, time_wait).until(
            lambda x: x.find_element(By.XPATH, "//span[contains(text(),'Export citation to RIS')]"))

        file = download_file_from_click_of_button(driver, ris_button)
        if file:
            shutil.move(file, output_filename)

        try:
            '''
            next_page_button = WebDriverWait(driver, time_wait).until(
                lambda x: x.find_element_by_xpath("//a[@data-aa-name='srp-next-page']"))
            '''
            ##AKA_Apr23: Change in Selenium 4.3.0: 
            next_page_button = WebDriverWait(driver, time_wait).until(
                lambda x: x.find_element(By.XPATH, "//a[@data-aa-name='srp-next-page']"))
            
            link = next_page_button.get_attribute('href')
            driver.get(link)
        except:
            break    
    '''
    for page_no in range(1, MAX_PAGES + 1):
        output_filename = os.path.join(output_directory, 'science_direct_auto_' + str(page_no) + '.ris')

        select_all_checkbox = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//label[@for='select-all-results']/span"))


        desired_y = (select_all_checkbox.size['height'] / 2) + select_all_checkbox.location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

        select_all_checkbox.click()

        export_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[@class='export-all-link-text']"))
        export_button.click()

        ris_button = WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath("//span[contains(text(),'Export citation to RIS')]"))

        file = download_file_from_click_of_button(driver, ris_button)
        if file:
            shutil.move(file, output_filename)

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                lambda x: x.find_element_by_xpath("//a[@data-aa-name='srp-next-page']"))
            link = next_page_button.get_attribute('href')
            driver.get(link)
        except:
            break
            '''

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
    ## Now using rsplit | y = txt.strip('https://www.sciencedirect.com/search?')
    ## link split char
    z = txt.rsplit('?')
    ## Note that z is a list
    ##//print(f'|link split is {z}')

    ## Note that sciencedirect signin redirect look like     ##https://www.sciencedirect.com/user/login?targetURL=%2Fsearch%3Foffset%3D25%26qs%3D%2528%2522digital%2520technologies%2522%2520OR%2520%2522Digital%2520technology%2522%2529%2520AND%2520%2528%2522definition%2522%2520OR%2520%2522define%2522%2520OR%2520%2522coined%2522%2529%26show%3D100&from=globalheader
    
    signin_prefix = 'https://www.sciencedirect.com/user/login?targetURL=%2Fsearch%3F'
    ##signin_split = str(z[1])
    sd_split = str(z[1]) ##sd link split
    print(f'In signin_link_url, sd_split (z[1]) is: {sd_split}')
    
    ##signin_split_join = ''.join(z[1]) ## currently using str()
    
    ## NB: doesn't work well | signin_url = signin_prefix + signin_split + '&from=globalheader'
    ## Unfortuantely, sciencedirect does not work with the rejoined url.
    ## We need to translate.
    
    ## choice of using chained str.replace or str.translate
    ##Translate make us of maketrans using replacement characters in dict
    ### See https://stackoverflow.com/questions/3411771/best-way-to-replace-multiple-characters-in-a-string
    
    '''
    ##TODO: changed hardcoded sd (sciencedirect url) to reference link from main
    ##AKA_Mar22: resolved assigning link to txt
    ##//sd = 'https://www.sciencedirect.com/search?qs=%28%22digital%20technologies%22%20OR%20%22Digital%20technology%22%29%20AND%20%28%22definition%22%20OR%20%22define%22%20OR%20%22coined%22%29'
    sd_split = sd.rsplit('?')
    print(f'\n sd split: {str(sd_split[1])}')
    ## https://www.sciencedirect.com/user/login?targetURL=%2Fsearch%3Fqs%3D%2528%2522digital%2520technologies%2522%2520OR%2520%2522Digital%2520technology%2522%2529%2520AND%2520%2528%2522definition%2522%2520OR%2520%2522define%2522%2520OR%2520%2522coined%2522%2529&from=globalheader

    ## https://www.sciencedirect.com/user/login?targetURL=%2Fsearch%3Fqs%3D%2528%2522digital%2520technologies%2522%2520OR%2520%2522Digital%2520technology%2522%2529%2520AND%2520%2528%2522definition%2522%2520OR%2520%2522define%2522%2520OR%2520%2522coined%2522%2529&from=globalheader    
        
    ##sd_rejoin_url = signin_prefix + str(sd_split[1]) + '&from=globalheader'
    ##print(f'\n SD rejoin url: {sd_rejoin_url}')
    '''

    ## AKA_Mar22: sd_split --> signin_split = str(z[1])
    sd_split1 = sd_split.translate(str.maketrans({'%': '%25', '=': '%3D'}))
    ##sd_split1 = signin_split.translate(str.maketrans({'%': '%25', '=': '%3D'}))
    sd_translate_url = signin_prefix + str(sd_split1) + '&from=globalheader'
    print(f'\n SD translated url: {sd_translate_url}')
    
    ##print(f'signin split: {signin_split}')
    ##print(f'signin split using join: {signin_split_join}')
    ##print(f'signin url: {signin_url}')
    ##print(f'translated signin url: {sd_translate_url}')
    
    ## choice of using chained str.replace or str.translate
    ## s = "abc&def#ghi" | print(s.translate(str.maketrans({'&': '\&', '#': '\#'})))
    
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
        
    ##AKA_Mar22: Moved to while loop
    ##print(f'In check_linkpage, catch_isElementPresent text: "{catch_isElementPresent.e_locator_text}"')
    ## fxn attribute outside of fxn
    ## See https://stackoverflow.com/questions/19326004/access-a-function-variable-outside-the-function-without-using-global/19327712
    
    '''
    ## AKA_Mar22: 
    if catch_isElementPresent.e_locator_text == 'Sign in' or 'Register':
        ##delay calling page directly. Allow for signing in
        signin_link = signin_link_url(link)
        ## change link to new link
        driver.get(signin_link)
        ## wait for time specified to enable log in before proceeding to download
        timewait = 25
        print(f'In check_linkpage, pausing for {timewait}s')
        time.sleep(timewait)
        print(f'In check_linkpage, going to download_acm_citations_from_search_link')
        download_acm_citations_from_search_link(driver, signin_link, output_dir)
    else:
        download_acm_citations_from_search_link(driver, link, output_dir)
        ##TODO: perhaps reuse existing session id
    return
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
    download_acm_citations_from_search_link(driver, link, output_dir)
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



def __main():
    ''' AKA_Feb22
    link = 'https://www.sciencedirect.com/search?qs=mutation%20testing&show=25&tak=%22mutation%20testing%22'
    output_dir = '.server_files/InputFiles/Science_direct'
    driver = getDriver(proxyFile='proxy_auth_plugin.zip')
    download_acm_citations_from_search_link(driver, link, output_dir)'''
    ''' AKA_Feb22
    link = 'https://www.sciencedirect.com/search?qs=%28%22digital%20technologies%22%20OR%20%22Digital%20technology%22%29%20AND%20%28%22definition%22%20OR%20%22define%22%20OR%20%22coined%22%29'
    '''
    ## AKA_Feb22 Show 100 results per page, offset (start from) result #26
    ##link = 'https://www.sciencedirect.com/search?offset=25&qs=%28%22digital%20technologies%22%20OR%20%22Digital%20technology%22%29%20AND%20%28%22definition%22%20OR%20%22define%22%20OR%20%22coined%22%29&show=100'
    
    ## AKA_Feb22: show 100 results per page
    ##link = 'https://www.sciencedirect.com/search?qs=%28%22digital%20technologies%22%20OR%20%22Digital%20technology%22%29%20AND%20%28%22definition%22%20OR%20%22define%22%29%20AND%20%28%22Digital%20Transformation%22%29&show=100'
    
    ## AKA_Mar22: show 100 results per page
    link = 'https://www.sciencedirect.com/search?qs=%28%22Digital%20technology%22%29%20AND%20%28define%20OR%20coined%29%20AND%20%28%22digital%20transformation%22%29&show=100'
    
    ##AKA_Feb22 | test for dir, if not create
    output_dir = '../../.server_files/InputFiles/Science_direct'
    createDirectoryIfNotExists(output_dir)
    print(f'output_dir created: {output_dir}')
    ##AKA_Feb22 | Disable use of proxy server
    ##driver = getDriver(proxyFile='proxy_auth_plugin.zip')
    ##driver = getDriver(proxyFile='../../proxy_auth_plugin.zip')
    driver = getDriver()
    
    ##AKA_Mar22: before utilising driver (Chrome session),
    ## Let's save some parameters, possibly for later use
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    print(f'driver url is: {executor_url} | session id is {session_id}')
    
    ##AKA_Feb22: check if author is logged in before calling download
    ##download_acm_citations_from_search_link(driver, link, output_dir)
    check_linkpage(driver, link, output_dir)
 


if __name__ == '__main__':
    sys.exit(__main())



        
'''
AKA_Feb22 || ##AKA_Apr23: Change in Selenium 4.3.0: 
        Using xpath:
        element = find_element_by_xpath("element_xpath")
        Needs be replaced with:
        element = driver.find_element(By.XPATH, "element_xpath")
        
        Deprecation Warning: find_element_by_* commands are deprecated. Please use find_element() instead         https://stackoverflow.com/questions/69875125/find-element-by-commands-are-deprecated-in-selenium
        
        You have to include the following imports
        from selenium.webdriver.common.by import By
        [Optional: if needing to seth chromedriver PATH]
        from selenium.webdriver.chrome.service import Service

        Using class_name:
        button = driver.find_element_by_class_name("quiz_button")
        Needs be replaced with:
        button = driver.find_element(By.CLASS_NAME, "quiz_button")

        Using id:
        element = find_element_by_id("element_id")
        Needs be replaced with:
        element = driver.find_element(By.ID, "element_id")

        Using name:
        element = find_element_by_name("element_name")
        Needs be replaced with:
        element = driver.find_element(By.NAME, "element_name")

        Using link_text:
        element = find_element_by_link_text("element_link_text")
        Needs be replaced with:
        element = driver.find_element(By.LINK_TEXT, "element_link_text")

        Using partial_link_text:
        element = find_element_by_partial_link_text("element_partial_link_text")
        Needs be replaced with:
        element = driver.find_element(By.PARTIAL_LINK_TEXT, "element_partial_link_text")

        Using tag_name:
        element = find_element_by_tag_name("element_tag_name")
        Needs be replaced with:
        element = driver.find_element(By.TAG_NAME, "element_tag_name")

        Using css_selector:
        element = find_element_by_css_selector("element_css_selector")
        Needs be replaced with:
        element = driver.find_element(By.CSS_SELECTOR, "element_css_selector")

        Using xpath:
        element = find_element_by_xpath("element_xpath")
        Needs be replaced with:
        element = driver.find_element(By.XPATH, "element_xpath")    
        '''