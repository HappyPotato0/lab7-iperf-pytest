import re

# Регулярка з методички - залишає тільки рядки з інтервалами трафіку
REGEXP = r'\[\s*[0-9]*\]\s*[0-9\.-]*\s*(sec)\s*[0-9\.]*\s*[A-Z]?(Bytes)\s*[0-9\.]*\s*[A-Z]?(bits/sec)\s*[0-9]*\s*[0-9\.]*\s*[A-Z]?(Bytes)'
KEYS = ('Interval', 'Transfer', 'Bitrate', 'Retr', 'Cwnd')


def to_mbytes(value, unit):
    # переводимо Transfer в MBytes
    if unit == 'GBytes':
        return value * 1024
    if unit == 'KBytes':
        return value / 1024
    return value


def to_mbits(value, unit):
    # переводимо Bitrate в Mbits/sec
    if unit == 'Gbits/sec':
        return value * 1000
    if unit == 'Kbits/sec':
        return value / 1000
    return value


def to_kbytes(value, unit):
    # переводимо Cwnd в KBytes
    if unit == 'MBytes':
        return value * 1024
    return value


def parser(output):
    result_list = []
    for line in output.split('\n'):
        if re.search(REGEXP, line):
            # прибираємо дужки, щоб "[  5]" не розбивалось на два елементи
            parts = line.replace('[', '').replace(']', '').split()
            # parts: ['5', '0.00-1.00', 'sec', '5.67', 'GBytes', '48.7', 'Gbits/sec', '0', '1.50', 'MBytes']
            interval = parts[1]
            transfer = to_mbytes(float(parts[3]), parts[4])
            bitrate = to_mbits(float(parts[5]), parts[6])
            retr = float(parts[7])
            cwnd = to_kbytes(float(parts[8]), parts[9])
            values = (interval, round(transfer, 2), round(bitrate, 2), retr, round(cwnd, 2))
            result_list.append(dict(zip(KEYS, values)))
    return result_list
