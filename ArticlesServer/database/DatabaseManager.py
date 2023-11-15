## AKA_Feb22 edited

## Load libraries
from .generate_articles_database import generate_articles_database_from_files


class DatabaseManager:
    _currentDatabase = None

    @staticmethod
    def get_instance():
        ##AKA_Feb22: added print to test
        print(f'In DBMgr get_instance...')
        return DatabaseManager._currentDatabase

    @staticmethod
    def reload_database():
        ##AKA_Feb22: added print to test
        print(f'In DBMgr reload_database... going to .generate_articles_db')
        
        '''
        AKA_Feb22:
        The reload_database fxn called (typically from __init__)
        attempts to generate articles db.
        In this instance, by getting articles (search per finder and link)
        This is done by calling the fxn (generate_articles_database_from_files)
        from generate_articles_database
        '''
        
        DatabaseManager._currentDatabase = generate_articles_database_from_files()
