# About This Repo
This is a simple utility that will simulate an SSH endpoint as a Ciena, Cisco, or Juniper with a very small command set.

# To Run This
* Download and install Linux (here Ubuntu)
* Install docker `apt-get install docker.io`
* Download this repo somewhere (here `/root/FakeTelnet`)
* Change to the directory `cd /root/FakeTelnet`
* Build the container `docker build -t gskyft .`
* Start the container `docker run -t -i -p 2222:22 --name ft gskyft`
* After that, you should be able to ssh to the server on port 2222

# Command Set
## Juniper
 * SSH into the device on port 2222 using username `juniper` and password `juniper0`
 * Enter configuration mode (`configure`)  
 * Set root password (`set system root-authentication plain-text-password newpassword`)
 * Hostname is customizable and when you commit, it will set the host name in the prompt  
 * Set hostname (`set system host-name JuniperMX480-01`)  
 * Set domain (`set system domain-name example.com`)  
 * Set default route (`set system backup-router 10.0.0.1`)  
 * Set default route (`set routing-options static route default nexthop 10.0.0.1 retain noreadvertise`)  
 * Save configuration (`commit`)

## Cisco
 * SSH into the device on port 2222 using username `cisco` and password `cisco`
 * Show interfaces (`show ip interface brief`)
 * Show interfaces (`show interface descriptions`)
 * Show terminal server hosts (`show hosts`)
 * Enter configure mode (`configure terminal`)
 * Add a new terminal server host (`ip host ciena3916 2048 192.168.1.1`)  
 * Exit configure mode (`end`)  
 * Save configuration (`write memory`)  
 * Enter any bad command and it will spit it back to you

## Ciena
 * SSH into the device on port 2222 using username `su` and password `wwp`
 * Create a VLAN (`vlan create vlan 100`)
 * Note that all VLAN numbers and ports (1-6) are usable for all these commands. Also note you must create the VLAN before adding it to a port. The script does not have logic to handle this  
 * Add VLAN to a port (`vlan add vlan 100 port 2`)  
 * See list of VLANs on which port (`vlan show`)  
 * Show statistics with fake counters (`port show port 2 statistics`) 
 * All ports share the same fake statistics. Once cleared, they will be zero for the rest of the SSH session. 
 * Reset fake counter statistics (`port clear port 2 statistics`)  
 * Remove VLAN from port (`vlan remove vlan 100 port 2`)
 * Be sure to remove the VLAN from the port before deleting. There is no logic to handle this  
 * Delete a VLAN (`vlan delete vlan 100`)  
 * Save configuration (`configuration save`)  
 * Enter any bad command and it will spit it back to you
