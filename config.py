# Stores the configuration information of the database
import logging
# Connecting to the database
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'pet-hospital'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,
                                                              PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# config loggin
logger = logging.getLogger('flask.app')
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("flask.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)




