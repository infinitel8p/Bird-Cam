## Using Wi-Fi Detection

### Setup Raspberry Pi as a Wi-Fi Access Point:

#### 1. **Install Required Packages**:
```bash
sudo apt-get update
sudo apt-get install hostapd dnsmasq
```

#### 2. **Configure Hostapd**:
- Edit the hostapd configuration file:
   ```bash
   sudo nano /etc/hostapd/hostapd.conf
   ```
- Add the following content, adjusting for your desired network name (SSID) and password:
   ```bash
   interface=wlan0
   driver=nl80211
   ssid=Your_Network_Name
   hw_mode=g
   channel=7
   wmm_enabled=0
   macaddr_acl=0
   auth_algs=1
   ignore_broadcast_ssid=0
   wpa=2
   wpa_passphrase=Your_Password
   wpa_key_mgmt=WPA-PSK
   wpa_pairwise=TKIP
   rsn_pairwise=CCMP
   ```
- Save the file and exit.  
  
#### 3. Configure Dnsmasq:
 - Backup the original dnsmasq configuration:
    ```bash
    sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
    ```
 - Create a new configuration:
    ```bash
    sudo nano /etc/dnsmasq.conf
    ```
 - Add the following content:
    ```bash
    interface=wlan0
    dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
    ```

#### 4. Set a Static IP Address for the wlan0 Interface:
- Edit the `dhcpcd` configuration file:
   ```bash
   sudo nano /etc/dhcpcd.conf
   ```

- Add the following to the bottom of the file, save, and exit:
   ```bash
   interface wlan0
   static ip_address=192.168.4.1/24
   nohook wpa_supplicant
   ```

#### 5. Start the Services:
```bash
sudo systemctl start hostapd
sudo systemctl start dnsmasq
```

#### 6. Enable Services to Start on Boot:
```bash
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

#### 7. Reboot:
```bash
sudo reboot
```

### Script Modification for Wi-Fi Detection:
To detect if a device is connected to the Raspberry Pi's Wi-Fi network, you can check the DHCP leases of dnsmasq:

```python
def is_device_connected_wifi():
    with open('/var/lib/misc/dnsmasq.leases', 'r') as f:
        if 'your_phone_mac_address' in f.read():
            return True
    return False
```
Replace 'your_phone_mac_address' with the MAC address of your phone.