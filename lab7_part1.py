import subprocess
import sys
import parser

server_ip = '127.0.0.1'


def client(server_ip, bitrate=None):
    # формуємо команду для iperf3 клієнта
    command = ['iperf3', '-c', server_ip, '-i', '1']
    if bitrate:
        command += ['-b', bitrate]  # обмеження швидкості, наприклад 10M
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()


bitrate = None
if len(sys.argv) > 1:
    bitrate = sys.argv[1]

result, error = client(server_ip, bitrate)

if error:
    print(error)
else:
    result_list = parser.parser(result)
    print('Всього інтервалів:', len(result_list))
    for value in result_list:
        if value['Transfer'] > 2 and value['Bitrate'] > 20:
            print(value)
