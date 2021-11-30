import requests, time, ast, mysql.connector, sys
from datetime import datetime

#MariaDB/MySQL connection details
try:
    db = mysql.connector.connect(
        host="",
        user="",
        passwd="",
        database=""
    )
    print("Successfully connected to Database..")
except:
    print("Error.. Can't connect to Database")
    sys.exit(1)

#Variables setup
#Interval in seconds
sys_timeframe_data = int(sys.argv[1])
#Item ID
sys_item_name_id = int(sys.argv[2])
#Currency ID (e.g. 1 = $, 3 = €)
sys_currency_id = int(sys.argv[3])
#Language (e.g. german) shouldn't matter
sys_language = sys.argv[4]
#Country (e.g. DE)
sys_country = sys.argv[5]

table_found = False

cursor = db.cursor()
item_db = str(sys_item_name_id) + "_" + str(sys_currency_id)
sql = "INSERT INTO " + item_db + " (date, bid, ask) VALUES (%s, %s, %s)"

#Check for existing table, if not create one
cursor.execute("SHOW TABLES")

for table_name in cursor:
    if table_name[0] == item_db:
        table_found = True
        print("Table " + item_db + " found..")
        break

if table_found == False:
    cursor.execute("CREATE TABLE " + item_db + """ (
        date datetime NOT NULL PRIMARY KEY,
        bid int(11) NOT NULL,
        ask int(11) NOT NULL)
    """)
    print("Table " + item_db + " created..")

print("Initial setup done.. collecting now data..")

#Get data from the steam community market
def getData(timeframe, itemid, currency, country, language):
    time.sleep(timeframe)
    try:
        response = requests.get("https://steamcommunity.com/market/itemordershistogram?country=" + str(country) + "&language=" + str(language) + "&currency=" + str(currency) + "&item_nameid=" + str(itemid) + "&two_factor=0")
        if response.status_code == 200:
            data = ast.literal_eval(str(response.json()))
            date_now = datetime.now()

            val = (str(date_now), data['highest_buy_order'], data['lowest_sell_order'])
            print(val)
            cursor.execute(sql, val)
            db.commit()
            print(cursor.rowcount, "record inserted.")
        else:
            print("Can't retrieve Data; Error: " + str(response.status_code))
    except requests.exceptions.ConnectionError:
        print("Connection Error.. Retrying in 60 Seconds")
        time.sleep(60)
    except mysql.connector.Error as error:
        print("Database Error: " + error)
    except:
        print("Something went wrong..")

#Startup
while True:
    getData(sys_timeframe_data, sys_item_name_id, sys_currency_id, sys_country, sys_language)