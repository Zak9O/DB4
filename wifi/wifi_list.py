import network

def check_all_wifis():

    """
    Scans for all available WiFi networks and prints their information.

    Returns:
    None
    """

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    # Scan for available networks
    available_networks = wifi.scan()
    print("Available Networks:")
    for net in available_networks:
        print(net)