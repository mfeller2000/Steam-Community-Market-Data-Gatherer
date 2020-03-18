import requests, time, ast, mysql.connector, sys
from datetime import datetime

#MariaDB/MySQL connection details
try: 
    db = mysql.connector.connect(
        host="host",
        user="user",
        passwd="password",
        database="database"
    )
    print("Successfully connected to database..")
except:
    print("Error.. cannot connect to database..")

#Variables setup
sys_timeframe_data = int(sys.argv[1])
sys_timeframe_ohlc = int(sys.argv[2])
sys_item_name = sys.argv[3]
sys_currency_id = int(sys.argv[4])
sys_app_id = int(sys.argv[5])

table_found = False

cursor = db.cursor()
item_db = str(sys_app_id) + "_" + str(sys_currency_id) + "_" + sys_item_name.replace("%20", "").replace("%29", "").replace("%28", "").replace("-", "")
sql = "INSERT INTO " + item_db + " (date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s)"

count = int(sys_timeframe_ohlc / sys_timeframe_data)

#Check for existing table, if not create one
cursor.execute("SHOW TABLES")

for table_name in cursor:
    if table_name[0] == item_db:
        table_found = True
        print("Table " + item_db + " found..")
        break

if table_found == False:
    cursor.execute("CREATE TABLE " + item_db + """ (
        id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        date datetime NOT NULL,
        open float NOT NULL,
        high float NOT NULL,
        low float NOT NULL,
        close float NOT NULL,
        volume int(11) NOT NULL)
    """)
    print("Table " + item_db + " created..")

print("Initial setup done.. collecting now data..")

#Get data from the steam community market
def getData(timeframe, item, currency, appid):
    time.sleep(timeframe)
    response = requests.get("https://steamcommunity.com/market/priceoverview/?appid=" + str(appid) + "&currency=" + str(currency) + "&market_hash_name=" + item)
    if response.status_code == 200:
        data = ast.literal_eval(str(response.json()))
    else:
        print("Status: " + str(response.status_code))
        data = {}
        
    return data

#Collect the data from getData() and process it to database
def getOHLC(timeframe_data, timeframe_ohlc, item, currency, appid):
    price = []
    for step in range(count):
        data = getData(timeframe_data, item, currency, appid)
        date_now = datetime.now()
        if len(data) > 0:
            data_volume = data['volume']
            price.append(float(data['lowest_price'][1:]))

    if len(price) > 0:
        print(price)
        val = (date_now, price[0], max(price), min(price), price[-1], data_volume)
        cursor.execute(sql, val)
        db.commit()
        print(cursor.rowcount, "record inserted.")
        print(str(date_now) + " - open: " + str(price[0]) + " high: " + str(max(price)) + " low: " + str(min(price)) + " close: " + str(price[-1]) + " volume: " + str(data_volume))

#Startup
while True:
    getOHLC(sys_timeframe_data, sys_timeframe_ohlc, sys_item_name, sys_currency_id, sys_app_id)
    #arg1: timeframe_data, arg2: timeframe_ohlc, arg3: item_name, arg4: currency_id, arg5: appid
