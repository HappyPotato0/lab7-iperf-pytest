import parser

# мінімальні значення для перевірки
TRANSFER_MIN = 2   # MBytes
BITRATE_MIN = 20   # Mbits/sec


class TestSuite():

    def test_iperf3_client_connection(self, client):
        result, error = client

        # перевіряємо що клієнт не повернув помилку
        assert error == '', 'Помилка клієнта: ' + error

        result_list = parser.parser(result)
        assert len(result_list) > 0, 'Парсер не знайшов жодного інтервалу'

        for value in result_list:
            print(value)
            assert value['Transfer'] > TRANSFER_MIN, 'Transfer менше ніж ' + str(TRANSFER_MIN) + ' в інтервалі ' + value['Interval']
            assert value['Bitrate'] > BITRATE_MIN, 'Bitrate менше ніж ' + str(BITRATE_MIN) + ' в інтервалі ' + value['Interval']
