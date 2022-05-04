import json, requests, pg8000
import re
import logging
from logging.handlers import TimedRotatingFileHandler
logger = logging.getLogger()
filehandler = TimedRotatingFileHandler('/Users/evan/project2/log/logging.log', 'D', 1, 60)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
# db config
try:
    with open('db_config.json', 'r') as f:
        DB_CONFIG = json.loads(f.read())
except: 
    DB_CONFIG = {
        "database": "postgres",
        "user": "evan",
        "password": "206803",
        "host": "127.0.0.1",
        "port": "5432"
    }
# api server config
try:
    with open('api_config.json', 'r') as f:
        API_CONFIG = json.loads(f.read())
except:
    API_CONFIG = {
        "server_url": "icemdev.retchat.com",
    }
    
SERVICE = "https://" + API_CONFIG["server_url"]+"/cksync/common/"

conn = pg8000.connect(database=DB_CONFIG["database"], user=DB_CONFIG["user"], password=DB_CONFIG["password"], host=DB_CONFIG["host"], port=DB_CONFIG["port"])
cursor = conn.cursor()
cursor.execute("select from tablename")
rows = cursor.fetchall()
# for loop deal 2 things
for row in rows:
    api1 = SERVICE+"?retUid="+row[1]+"&otherId="+row[0] # cookies + line_uid
    api2 = SERVICE+"?retUid="+row[1]+"&otherId="+row[2] # cookies + memberid
    try:
        res1 = requests.get(api1).json()
        res2 = requests.get(api2).json()
        # do something with res1 and res2
    except:
        logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.DEBUG)

conn.commit()
conn.close()
exit()

