from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import mysql.connector
import hashlib
import random
import string

sessions = {}
class SimpleRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type="text/json"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()
    
    def _generate_session_id(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            
            data = json.loads(post_data)        
            username = data.get('username')
            password = data.get('password')     
            # Connect to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="@",
                database="web"
            )       
            mycursor = db.cursor()      
            # Fetch the hashed password from the database
            mycursor.execute("SELECT password FROM userdata WHERE username = %s", (username,))
            result = mycursor.fetchone()  
            if result:
                stored_password = result[0]     
                # Hash the provided password
                hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()      
                # Compare the hashed passwords
                if hashed_password == stored_password:
                    session_id = self._generate_session_id()
                    sessions[session_id] = {'username': username}
                    self._set_response(200)
                    self.wfile.write(json.dumps({'message': 'Login successful', 'session_id': session_id}).encode('utf-8'))
                else:
                    self._set_response(401)
                    self.wfile.write(json.dumps({'message': 'Invalid credentials'}).encode('utf-8'))
            else:
                self._set_response(401)
                self.wfile.write(json.dumps({'message': 'Invalid credentials'}).encode('utf-8'))        
            db.close()

        if self.path == '/add_bookmark':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            url = data["url"]
            name = data["name"]
            sessionID = data['sessionID']
            session_data = sessions.get(sessionID, None)
            username = session_data.get('username', None)

            if username is not None:
                # Connect to the database
                db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="@",
                database="web")

                mycursor = db.cursor()

                sql = "INSERT INTO bookmark (name, url, username) VALUES (%s, %s, %s)"
                val = (name, url, username)

                mycursor.execute(sql, val)
                db.commit()

                self._set_response()
                self.wfile.write(json.dumps({"status": "Success", "message": "Bookmark added successfully"}).encode("utf-8"))
            else:
                self._set_response(401)
                self.wfile.write(json.dumps({'message': 'Invalid session'}).encode('utf-8'))

        if self.path == '/check':
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@",
            database="web")
            mycursor = mydb.cursor()
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            sessionID = data['sessionID']
            session_data = sessions.get(sessionID, None)
            username = session_data.get('username', None)            
            link=data['link']
            mycursor.execute("SELECT url FROM site WHERE username = %s", (username,))
            mysite = mycursor.fetchall()
            self._set_response()
            mycursor.execute("SELECT realtime_block FROM userdata WHERE username = %s", (username,))
            blockrealtimedata = mycursor.fetchall()
            first_item = blockrealtimedata[0]
            first_attribute_value = first_item[0]
            blockrealtimedata=False
            if(first_attribute_value ==1):
                blockrealtimedata=True
            if(blockrealtimedata):
                apiKey = 'AIzaSyD_sBfydgE1kbg5y1xAPKJFRXZB8hH4fQc'
                api_url = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={apiKey}'
                threat_info = {
                    'client': {'clientId': 'SafeWebNavigation', 'clientVersion': '1.0.0'},
                    'threatInfo': {
                        'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING','UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'],
                        'platformTypes': ['ANY_PLATFORM'],
                        'threatEntryTypes': ['URL'],
                        'threatEntries': [{'url': link}]
                    }
                }
                response = requests.post(api_url, json=threat_info)
                if response.ok:
                    data = response.json()
                    if 'matches' in data:
                        self.wfile.write(json.dumps({"block": True, 'why': f"this site blocked because of {data.get('matches')[0].get('threatType')}"}).encode("utf-8"))
                        return
            print(mysite)
            for site_tuple in mysite:
                site = site_tuple[0]  # Extract the string from the tuple
                if site in link:
                    self.wfile.write(json.dumps({"block": True,'why':'this site blocked from admin'}).encode("utf-8"))
                    return

            mycursor.execute("SELECT name FROM content WHERE username = %s", (username,))
            mycontent = mycursor.fetchall()
            url = f"https://website-categorization.whoisxmlapi.com/api/v3?apiKey=at_JzDY9mrdoi3JGHRrU3BwQh4XjoutW&url={link}"
                    
            response = requests.request("GET", url)

            response_json = json.loads(response.text)
            mydb.close()


            clas = response_json["categories"][0]["name"] 
            if (clas,) in mycontent:
                self.wfile.write(json.dumps({"block": True,'why':f'{clas} sites blocked from admin'}).encode("utf-8"))
                return
            
            self.wfile.write(json.dumps({"block": False}).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=SimpleRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
