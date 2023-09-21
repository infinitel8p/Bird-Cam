## Step 1: Install Required Packages
```bash
sudo apt-get update
sudo apt-get install hostapd dnsmasq
```

## Step 2: Create the Switching Script  
This script will:  
- Try to connect to known networks.  
- If it can't connect, it will switch to AP mode.

#### 1. Create the Script
```bash
sudo nano /usr/local/bin/wifi_switcher.sh
```

Add the following content and replace `'YOUR_HOME_WIFI_SSID1'` with your actual home SSID:  
(You could also add multiple SSIDs to the array, e.g., `('SSID1' 'SSID2' 'SSID3')`)

```bash
#!/bin/bash
echo "--- $(date) - Script started with PID $$  ---" >> /tmp/wifi_switcher.log

# Define an array of SSIDs
HOME_SSIDS=('YOUR_HOME_WIFI_SSID1')

# Initialize a flag to indicate if a home network is found
home_network_found=0

# Delay for 180 seconds
echo "$(date) - Initialization done. Sleeping for 2 min before running." >> /tmp/wifi_switcher.log
sleep 180

# Check for home networks
echo "$(date) - Checking for home networks" >> /tmp/wifi_switcher.log

# Scan for available networks and save the results to a variable
scan_results=$(sudo iwlist wlan0 scan | grep ESSID)

# Log the scan results and iwconfig output
echo "$scan_results" >> /tmp/wifi_switcher.log

# Check the scan results for each SSID in the HOME_SSIDS array
for ssid in "${HOME_SSIDS[@]}"; do
    echo "$scan_results" | grep -q "$ssid"
    if [ $? -eq 0 ]; then
        home_network_found=1
        break
    fi
done

if [ $home_network_found -eq 1 ]; then
    # Home network found
    echo "$(date) - Home network found. Stopping services." >> /tmp/wifi_switcher.log
    sudo systemctl stop hostapd
    sudo systemctl stop dnsmasq
else
    # Home network not found, start AP mode
    echo "$(date) - Home network not found. Starting services." >> /tmp/wifi_switcher.log
    sudo systemctl start hostapd
    sudo systemctl start dnsmasq
fi

echo "--- $(date) - Script finished ---" >> /tmp/wifi_switcher.log
```

Make the script executable:

```bash
sudo chmod +x /usr/local/bin/wifi_switcher.sh
```

#### 2. Schedule the Script
We'll use `cron` to run our script periodically:
```bash
sudo crontab -e
```

Add the following line to the end of the file to run the script every 4 minutes:

```bash
*/4 * * * * sudo /usr/local/bin/wifi_switcher.sh
```

## Step 3: Configure Hostapd for AP Mode
#### 1. Edit the `hostapd` configuration file:
```bash
sudo nano /etc/hostapd/hostapd.conf
```

Add the following content and replace `DevAccessPoint` and `YOUR_AP_PASSWORD` with your desired values:

```conf
interface=wlan0
driver=nl80211
ssid=DevAccessPoint
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=YOUR_AP_PASSWORD
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

#### 2. Specify where `hostapd` should find its configuration:
```bash
sudo nano /etc/default/hostapd
```

Find the line with `#DAEMON_CONF=""` and replace _(uncomment it or add it if it doesn't exist)_ it with: 

```bash
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

## Step 4: Configure Dnsmasq for DHCP in AP Mode
#### 4.1. Backup the original `dnsmasq` configuration:
```bash
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
```

#### 4.2. Create a new dnsmasq configuration:
```bash
sudo nano /etc/dnsmasq.conf
```

Add the following content:

```conf
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```

## Step 5: Configure a Static IP for the `wlan0` Interface
#### 5.1. Edit the `dhcpcd` configuration file:
```bash
sudo nano /etc/dhcpcd.conf
```

#### 5.2. Add the following content to the end of the file, save, and exit:
**_If you have previously changed the SSID in the [hostapd](#step-3-configure-hostapd-for-ap-mode) configuration file, you'll need to change the SSID in the `ssid` line below as well._**
```conf
# Use a static IP for AP mode
profile static_ap
static ip_address=192.168.4.1/24

# Set the profile based on the SSID
interface wlan0
ssid DevAccessPoint
use_profile static_ap
```

## Step 6: Restart the Services
#### 6.1. Restart `hostapd` and `dnsmasq`:
```bash
sudo systemctl restart dnsmasq
sudo systemctl restart hostapd
```

##### Note: If you get an error when restarting `hostapd` (_Failed to restart hostapd.service: Unit hostapd.service is masked._), try running the following commands:
- Unmask the `hostapd` service:
    ```bash
    sudo systemctl unmask hostapd
    ```
- Enable the `hostapd` service to start on boot:
    ```bash
    sudo systemctl enable hostapd
    ```
- This is where the ssh connection can be lost. After manually restarting the Pi, you should then see a network named `DevAccessPoint` (or whatever SSID name you've set) in the list of available Wi-Fi networks and connect to it using the password you've set.
  - SSH into the Pi using the static IP address you've set (e.g., `192.168.4.1`).
  - Once connected, check the status of both services to ensure they're running correctly:
      ```bash
      sudo systemctl status hostapd
      sudo systemctl status dnsmasq
      ```

#### 6.2. Check the logs:
```bash
cat /tmp/wifi_switcher.log
```

You should see something like this:
```log
--- Thu 21 Sep 17:28:01 CEST 2023 - Script started with PID [PID1]  ---
Thu 21 Sep 17:28:01 CEST 2023 - Initialization done. Sleeping for 2 min before running.
Thu 21 Sep 17:31:01 CEST 2023 - Checking for home networks
                    ESSID:"NETWORK_SSID_1"
                    ESSID:"NETWORK_SSID_2"
                    ...
                    ESSID:"NETWORK_SSID_N"
Thu 21 Sep 17:31:03 CEST 2023 - Home network found. Stopping services.
--- Thu 21 Sep 17:31:04 CEST 2023 - Script finished ---
--- Thu 21 Sep 17:32:01 CEST 2023 - Script started with PID [PID2]  ---
Thu 21 Sep 17:32:01 CEST 2023 - Initialization done. Sleeping for 2 min before running.
Thu 21 Sep 17:35:01 CEST 2023 - Checking for home networks
                    ESSID:"NETWORK_SSID_1"
                    ESSID:"NETWORK_SSID_2"
                    ...
                    ESSID:"NETWORK_SSID_N"
Thu 21 Sep 17:35:02 CEST 2023 - Home network found. Stopping services.
--- Thu 21 Sep 17:35:02 CEST 2023 - Script finished ---
--- Thu 21 Sep 17:36:02 CEST 2023 - Script started with PID [PID3]  ---
Thu 21 Sep 17:36:02 CEST 2023 - Initialization done. Sleeping for 2 min before running.
```

When in your home network, you should see it continuously logging `Home network found. Stopping services.` every 4 minutes.  
When not in your home network, you should see it logging `Home network not found. Starting services.` every 4 minutes.

You can ssh into the Pi in AP mode with the static IP address you've set (e.g., `192.168.4.1`) and if in your home network (Client mode) you can ssh into the Pi using its IP address in your home network.

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
