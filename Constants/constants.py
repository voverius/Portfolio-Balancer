from os import path


DATABASE_DIR = path.realpath(__file__).replace('Constants\constants.py', 'Database\Data.db')
CONFIG_FILE_DIR = path.realpath(__file__).replace('Constants\constants.py', 'ConfigFiles\\net_config.json')

LAMBDA = 1e-4  # lambda in loss function 5 in training

# About time
NOW = 0
SECOND = 1
HALF_MINUTE = SECOND * 30
MINUTE = HALF_MINUTE * 2
FIVE_MINUTES = MINUTE * 5
TEN_MINUTES = MINUTE * 10
FIFTEEN_MINUTES = FIVE_MINUTES * 3
HALF_HOUR = FIFTEEN_MINUTES * 2
HOUR = HALF_HOUR * 2
TWO_HOUR = HOUR * 2
FOUR_HOUR = HOUR * 4
DAY = HOUR * 24
WEEK = DAY * 7
YEAR = DAY * 365

# Trading table name
TABLE_NAME = 'test'

