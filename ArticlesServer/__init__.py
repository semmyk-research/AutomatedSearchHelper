## AKA_Feb22: include msg on terminal to indicate start page
import os

from flask import Flask
from flask_jsglue import JSGlue
from requests import Session

from TextSearchEngine.parse_finder import parse_finder
from AutomatedSearchHelperUtilities.configuration import configureLogger
from AutomatedSearchHelperUtilities.extract_doi_from_csv import extract_doi_from_csv
from AutomatedSearchHelperUtilities.utilities import createDirectoryIfNotExists
from .directories import BASE_DIRECTORY, DOIS_FILE, FINDER_FILE, INPUT_FILES_DIRECTORY, PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES

ALLOWED_EXTENSIONS = {'csv'}

'''
## AKA_Feb22
## https://stackoverflow.com/questions/61584680/flask-not-activating-debug-mode
if __name__ == "__main__":
    app.run(debug=True)
'''

def create_app(test_config=None):

    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        print ('creating dir ' + BASE_DIRECTORY )
        createDirectoryIfNotExists(BASE_DIRECTORY)
        createDirectoryIfNotExists(INPUT_FILES_DIRECTORY)
        for _, directory, _ in PUBLISHER_INPUT_DIRECTORIES_AND_FILE_TYPES:
            createDirectoryIfNotExists(directory)
        configureLogger()
        try:
            from ArticlesServer.database.DatabaseManager import DatabaseManager
            print('Database reload start')
            DatabaseManager.reload_database()
            '''
            AKA_Feb22:
            The reload_database fxn in DatabaseManager class
            will attempt getting (search and autodownload) articles
            based on the finder (search string) and link
            '''
            
            print('Successfully reloaded articles')
            
            ## AKA_Feb22: added print for testing purposes
            print('\nUsers can register under http://127.0.0.1:5000/register and login under http://127.0.0.1:5000/login')
            print('Press Ctrl+C to exit \n')
            ##print('\n')
        except Exception as e:
            print(e)
            print("Could not load old configuration")

    app = Flask(__name__, instance_relative_config=True)
    jsglue = JSGlue(app)

    '''
    ##AKA_Feb22: Attempting to force debug mode to True
    if __name__ == "__main__":
        app.run(debug=True)
    elif __name__ == "__ArticleServer__":
        app.run(debug=True)
    elif __name__ == "__create_app__":
        app.run(debug=True)
        
        ## These did not work.
    ## TODO: troubleshoot further
    
    ## For now, on Anaconda prompt, execute below after 'set FLASK_APP=ArticlesServer' and just before 'flask run'
    ##set FLASK_DEBUG=1 OR set FLASK_ENV=development
    ## 'set' is for Win. On other OS, use 'export'
    '''
    
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = 'super secret key'
    sess = Session()

    from .main import main
    app.register_blueprint(main)

    return app
