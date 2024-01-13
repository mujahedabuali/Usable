import mysql.connector
import hashlib

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@",
    database="web"
)

mycursor = mydb.cursor()


# mycursor.execute("""
# CREATE TABLE IF NOT EXISTS userdata(
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(255) NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     email VARCHAR(255) NOT NULL,
#     phonenumber VARCHAR(20) NOT NULL,
#     realtime_block boolean NOT NULL ,
#     macAddress VARCHAR(255) )
# """)



# username1, password1, email1, phonenumber1 = "issa", hashlib.sha256("Issa123".encode()).hexdigest(), "issaabed3322@gmail.com", "0599479422"
# username2, password2, email2, phonenumber2 = "mujahed", hashlib.sha256("Mujahed123".encode()).hexdigest(), "mujahedabuali0@gmail.com", "0597936305"
# username3, password3, email3, phonenumber3 = "rami", hashlib.sha256("Rami123".encode()).hexdigest(), "r4mimu701@gmail.com", "0597972396"
# username4, password4, email4, phonenumber4 = "adham", hashlib.sha256("adham123".encode()).hexdigest(), "mhudeibibrahim@gmail.com", "0597936306"

# sql = "INSERT INTO userdata (username, password, email, phonenumber, realtime_block) VALUES (%s, %s, %s, %s, %s)"
# values = (username1, password1, email1, phonenumber1, False)
# values1 = (username2, password2, email2, phonenumber2, False)
# values2 = (username3, password3, email3, phonenumber3, False)
# values3 = (username4, password4, email4, phonenumber4, False)

# mycursor.execute(sql, values)
# mycursor.execute(sql, values1)
# mycursor.execute(sql, values2)
# mycursor.execute(sql, values3)

# mydb.commit()  
