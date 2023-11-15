## AKA_Feb22
#!/usr/bin/env python

"""
Downloads articles from input, to given folder in .json format
"""

import argparse
import sys
import logging
from AutomatedSearchHelperUtilities.extract_doi_from_csv import extract_doi_from_csv
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
import AutomatedSearchHelperUtilities.configuration as configuration
from ArticlesDataDownloader.ArticlesDataDownloader import ArticlesDataDownloader
from ArticlesDataDownloader.read_input_file import read_input_file


def run_articles_download(outputArticles, article_datas, proxyFile=None):
    createDirectoryIfNotExists(outputArticles)
    downloader = ArticlesDataDownloader(outputArticles, proxyFile)
    return [downloader.read_article(article_data)[0] for article_data in article_datas]
'''
AKA_Feb22
##change arg proxyFile to 'optional' by setting a default value
def run_articles_download(outputArticles, article_datas, proxyFile):
    createDirectoryIfNotExists(outputArticles)
    downloader = ArticlesDataDownloader(outputArticles, proxyFile)
    return [downloader.read_article(article_data)[0] for article_data in article_datas]
'''

'''
##AKA_Feb22: webdriver Selenium Proxy uncheck by default | options.addArguments("--no-proxy-server"); | See https://amolchavan.space/post/selenium/uncheck-proxy-server-settings-in-chrome-browser-using-selenium-webdriver/
'''

def getArgumentsParser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--output_articles', default='outputArticles', type=str, help='Location for articles .json files')
    ## AKA_Feb22: change arg --proxy_file to no-proxy-server 11Feb22
    parser.add_argument('--no-proxy-server')
    ##parser.add_argument('--articles_list', default='DT-define_GS-search-08Feb22-02.2.ris', type=str, help='file containing articles data in supported format')
    ##AKA_Apr23: redirect default article list to a small list
    parser.add_argument('--articles_list', default='doi_ScienceDirect_article_list_test.ris', type=str, help='file containing articles data in supported format')
    parser.add_argument('--file_type', default=3, type=int, help='File format: '
                                                                 '1- SCOPUS_CSV (default), '
                                                                 '2- IEEE_CSV '
                                                                 '3- SCIENCE_DIRECT_RIS, '
                                                                 '4- SPRINGER_CSV'
                                                                 '5- WILLEY_RIS'
                                                                 '6- ACM_BIB')
    '''
    ##AKA_Feb22
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument('--output_articles', default='outputArticles', type=str, help='Location for articles .json files')
    parser.add_argument('--proxy_file', default='proxy_auth_plugin.zip', type=str, help='Proxy configuration file')
    ##parser.add_argument('--articles_list', default='scopus.csv', type=str, help='file containing articles data in supported format')
    parser.add_argument('--file_type', default=1, type=int, help='File format: '
                                                                 '1- SCOPUS_CSV (default), '
                                                                 '2- IEEE_CSV '
                                                                 '3- SCIENCE_DIRECT_RIS, '
                                                                 '4- SPRINGER_CSV'
                                                                 '5- WILLEY_RIS'
                                                                 '6- ACM_BIB')
                                                                 '''

    return parser


def main(args = None):
    configuration.configureLogger()
    logger = logging.getLogger('run_articles_download')

    p = getArgumentsParser()
    a = p.parse_args(args=args)

    logger.info("Starting run_articles_download with following arguments")
    logger.info("output_articles = " + a.output_articles)

    article_datas = read_input_file(a.articles_list, a.file_type)
    logger.info("doi_list = " + str(article_datas))

    ##AKA_Feb22: Let us for now disable use of proxy since we are not using Proxy Server
    ##AKA_Feb22 run_articles_download(a.output_articles, article_datas, a.proxy_file)
    ##AKA_Feb22: edit run_articles_download function above to accept 2 or 3 args
    run_articles_download(a.output_articles, article_datas)


if __name__ == '__main__': sys.exit(main())
