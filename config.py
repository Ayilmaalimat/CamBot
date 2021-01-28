import mysql.connector

API_TOKEN = ''

try:

    connect = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="toor1976",
        database="ComBot",
        auth_plugin='mysql_native_password'
    )

    DB = connect.cursor(buffered=True)

except Exception as e:
    print(f"--> Error connection to databases! \n Error:{e}")
