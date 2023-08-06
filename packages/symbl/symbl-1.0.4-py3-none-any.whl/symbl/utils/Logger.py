import logging

class Log():

    __instance = None
    __logger = None

    @staticmethod
    def getInstance():
        if Log.__instance == None:
            return Log()
            
        return Log.__instance

    def __init__(self):

        # logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(process)s - %(levelname)s - %(asctime)s - %(message)s', level=logging.INFO)
        if Log.__instance != None:
            raise Exception("Can not instantiate more than once!")

        # Log.__instance = self

        # Create a custom logger
        logger = logging.getLogger('my-logger')

        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('file.log')
        c_handler.setLevel(logging.NOTSET)
        f_handler.setLevel(logging.NOTSET)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        self.__logger = logger

    def info(self, data, *args):
        print("Logging info", data)
        self.__logger.info(data)

    def debug(self, data, *args):
        self.__logger.debug(data, args)

    def warning(self, data, *args):
        self.__logger.warning(data, args)
    
    def error(self, data, *args):
        self.__logger.error(data, args)