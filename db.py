import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="M23456",
  database="web"
)

mycursor = mydb.cursor()