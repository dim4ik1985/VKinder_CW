import os

from dotenv import load_dotenv

load_dotenv()

TOKEN_VK = os.getenv('VK_TOKEN')
DB_NAME = os.getenv('DB_NAME')
DB_USER_NAME = os.getenv('USER_NAME')
DB_PASS = os.getenv('PASSWORD')