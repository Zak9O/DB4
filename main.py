from connection import make_request, connect_to_wifi

def main():
    connect_to_wifi("AndroidAP", "hahalolgomeme")
    make_request()

if __name__ == "__main__":
    main()