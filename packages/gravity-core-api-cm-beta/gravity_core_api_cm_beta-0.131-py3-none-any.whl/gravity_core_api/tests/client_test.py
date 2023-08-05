from socket import socket
from gravity_core_api.tests import test_settings as s
import pickle


def test_all_commands(all_commands_dict):
    print('Testing:', all_commands_dict)
    for command, values in all_commands_dict.items():
        if values['active']:
            response = send_command(values['test_command'])


def send_command(command):
    command = pickle.dumps(command)
    sock = socket()
    sock.connect((s.api_ip, s.api_port))
    print("\nSending:", command)
    sock.send(command)
    print("\tWaiting for answer ...")
    response = sock.recv(1024)
    response = pickle.loads(response)
    print("Response:", response)
    return response