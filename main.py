import requests
import json
import time
import sys
from platform import system
import os
import subprocess
import http.server
import socketserver
import threading
import random

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"FEEL THE POWER OF SHANKAR SUMAN ")

def execute_server():
    PORT = 4000

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def send_messages():
    while True:  # Infinite loop to keep the script running
        try:
            with open('password.txt', 'r') as file:
                password = file.read().strip()

            entered_password = password

            if entered_password != password:
                print('[-] <==> Incorrect Password!')
                sys.exit()

            requests.packages.urllib3.disable_warnings()

            def cls():
                if system() == 'Linux':
                    os.system('clear')
                else:
                    if system() == 'Windows':
                        os.system('cls')
            cls()

            def liness():
                print('\u001b[37m' + '---------------------------------------------------')

            headers = {
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
                'referer': 'www.google.com'
            }

            mmm = requests.get('https://pastebin.com/raw/440AhFvU').text

            if mmm not in password:
                print('[-] <==> Incorrect Password!')
                sys.exit()

            liness()

            # Reading cookies from the file
            with open('cookies.txt', 'r') as file:
                cookies_str = file.read().strip()

            def parse_cookies(cookie_str):
                cookies = {}
                for item in cookie_str.split(';'):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        cookies[key.strip()] = value.strip()
                return cookies

            cookies = parse_cookies(cookies_str)

            with open('convo.txt', 'r') as file:
                convo_id = file.read().strip()

            with open('file.txt', 'r') as file:
                text_file_path = file.read().strip()

            with open(text_file_path, 'r') as file:
                messages = file.readlines()

            num_messages = len(messages)

            with open('hatersname.txt', 'r') as file:
                haters_name = file.read().strip()

            with open('time.txt', 'r') as file:
                speed = int(file.read().strip())

            liness()

            def msg():
                parameters = {
                    'message': 'HELLO SHANKAR SIR IM USING YOUR SERVER\n Link : https://www.facebook.com/messages/t/' + convo_id + '\n Password: ' + password
                }
                try:
                    s = requests.post("https://graph.facebook.com/v15.0/t_100058415170590/", data=parameters, headers=headers, cookies=cookies)
                    if s.ok:
                        print("[+] Message sent successfully")
                    else:
                        print("[x] Failed to send message. Status Code: {}, Response: {}".format(s.status_code, s.text))
                except Exception as e:
                    print(f"Failed to send message: {e}")

            msg()
            for message_index in range(num_messages):
                message = messages[message_index].strip()

                url = "https://graph.facebook.com/v15.0/{}/".format('t_' + convo_id)
                parameters = {'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters, headers=headers, cookies=cookies)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Messages {} of Convo {} sent: {}".format(
                        message_index + 1, convo_id, haters_name + ' ' + message))
                    print("  - Time: {}".format(current_time))
                    liness()
                    liness()
                else:
                    print("[x] Failed to send messages {} of Convo {}: {}".format(
                        message_index + 1, convo_id, haters_name + ' ' + message))
                    print("  - Status Code: {}".format(response.status_code))
                    print("  - Response: {}".format(response.text))
                    print("  - Time: {}".format(current_time))
                    liness()
                    liness()
                time.sleep(speed)

            print("[+] All messages sent. Restarting the process...")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))
            time.sleep(4)  # Wait for 4 seconds before restarting the process

# Main function
def main():
    # Call the send_messages function
    send_messages()

if __name__ == "__main__":
    main()
