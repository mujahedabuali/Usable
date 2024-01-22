from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import mysql.connector



class SimpleRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type="text/json"):
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_POST(self):
        if self.path == '/add_bookmark':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            url = data["url"]
            name = data["name"]

            # Connect to the database
            db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="issa",
            database="web")

            mycursor = db.cursor()

            sql = "INSERT INTO bookmark (name, url) VALUES (%s, %s)"
            val = (name, url)
    
            mycursor.execute(sql, val)
            db.commit()

            self._set_response()
            self.wfile.write(json.dumps({"status": "Success", "message": "Bookmark added successfully"}).encode("utf-8"))

        if self.path == '/check':
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="issa",
            database="web")
            mycursor = mydb.cursor()
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            mycursor.execute("SELECT url FROM site")
            mysite = mycursor.fetchall()
            self._set_response()
            link=data['link']
            mycursor.execute("SELECT realtime_block FROM userdata")
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
                        self.wfile.write(json.dumps({"block": True, 'why': f'this site blocked because of {data.get('matches')[0].get('threatType')}'}).encode("utf-8"))
                        return
            if(link,) in mysite:
                self.wfile.write(json.dumps({"block": True,'why':'this site blocked from admin'}).encode("utf-8"))
                return

            mycursor.execute("SELECT name FROM content")
            mycontent = mycursor.fetchall()
            url = f"https://website-categorization.whoisxmlapi.com/api/v3?apiKey=at_KRngxoDlqI3U5RBQMytkwcdirsO58&url={link}"
                    
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
