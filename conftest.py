import subprocess
import time

import paramiko
import pytest

# дані для підключення по ssh (сервер на цій же віртуалці)
server_ip = '127.0.0.1'
username = 'vadym'
password = 'qwertyuiop'

# команда для запуску iperf3 сервера (-D - запуск у фоні)
server_command = 'iperf3 -s -D'


@pytest.fixture(scope='function')
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_ip, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command(server_command)
    error = stderr.read().decode()
    time.sleep(1)  # чекаємо поки сервер підніметься

    yield error

    # teardown - зупиняємо iperf3 сервер і закриваємо ssh
    stdin, stdout, stderr = ssh.exec_command('pkill iperf3')
    stdout.channel.recv_exit_status()  # чекаємо поки команда виконається
    ssh.close()


@pytest.fixture(scope='function')
def client(server):
    process = subprocess.Popen(['iperf3', '-c', server_ip, '-i', '1'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()
