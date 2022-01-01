import mysql.connector
def credentials():
	mydb = mysql.connector.connect(
	  host="localhost",
	  user="user",
	  password="password",
	  database="database"         )
	return mydb
