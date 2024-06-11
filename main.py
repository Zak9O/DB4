from connection import connect_to_wifi, publish_and_subscribe_to_adafruit_io
from wifi_list import check_all_wifis

def main():
    check_all_wifis()
    connect_to_wifi('Oscar iPhone', '123456789')
    publish_and_subscribe_to_adafruit_io('linusjuni', 'aio_hEHF11FSb8mtj9G6NMuiSIGJJlvh', 'dtu-db4')

if __name__ == "__main__":
    main()

