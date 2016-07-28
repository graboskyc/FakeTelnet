#!/usr/bin/python

import time
import collections
import sys

class Port:
	def __init__(self, num):
		self.PortNum = num
		self.VLANS = []

	def AddVLAN(self, vlan):
		if vlan not in self.VLANS:
			self.VLANS.append(vlan)
			self.VLANS.sort()

	def RemoveVLAN(self, vlan):
		self.VLANS.remove(vlan)
		self.VLANS.sort()

	def DEBUG(self):
		print self.PortNum
		print self.VLANS

class VLAN:
        def __init__(self, num):
                self.VLAN = num
                self.Ports = []

        def AddPort(self, p):
                if p not in self.Ports:
                        self.Ports.append(p)
                        self.Ports.sort()

        def DEBUG(self):
                print self.VLAN
                print self.Ports

class Switch:
	def __init__(self, ip, vendor):
		self._ports = []
		self._ip = ""
		self._model = ""
		self._hostname = ""
		self._currPrompt = ""
		self._badPrompt = ""
		self._vlans = []
		self._hosts = []
		
		self._ip = ip
		ipArray = ip.split(".")

		print "Trying %s..." %(ip)
		print "Connected to %s." %(ip)
		print "Escape character is '^]'."
		print ""

		if (vendor == 'ciena'):
			self._model = "ciena"
			self._hostname = "Ciena3916_" + str(ipArray[3])
			self._currPrompt = self._hostname + ">"
			self._badPrompt = "SHELL PARSER FAILURE: '%s' - invalid input"

			i = 1
			while ( i < 7 ):
				self._ports.append(Port(i))
				i=i+1

			if (len(ipArray[3]) == 1):
				mac = "0"+str(ipArray[3])
			elif (len(ipArray[3]) == 2):
				mac = str(ipArray[3])
			elif (len(ipArray[3]) == 3):
				mac = str(ipArray[3])[1:]
			else:
				mac = "aa"
			print "Ciena %s 00:23:8A:57:A5:%s" %(self._hostname, mac)
			print "SAOS is True Carrier Ethernet TM software.\n"
			print "%s login: su" %(self._hostname)
			print "Password: "

			print "SAOS is True Carrier Ethernet TM software."
			print "Welcome to the shell."

		elif (vendor == 'ios'):
			self._model = "ios"
			self._hosts = []
			self._hostname = "Cisco2600_" + str(ipArray[3])
                        self._currPrompt = self._hostname + ">"
			self._badPrompt = "% Bad IP address or host name% Unknown command or computer name, or unable to find computer address"

			print ""
			print "User Access Verification"
			print ""
			print "Username: cisco"
			print "Password: "
			print self._currPrompt + "enable"
			print "Password:"
			self._currPrompt = self._hostname + "#"
		elif (vendor == 'juniper'):
			self._model = "juniper"
			self._currPrompt = "\n{master}\nroot@>"

			print
			print "(ttyp0)"
			print
			print "login: root"
			print "Password: "
			print
			print "--- JUNOS 9.6R4.4 built 2010-05-28 08:10:35 UTC"
		elif (vendor == 'xr'):
			self._model = "xr"
	def GenerateVLANObj(self):
		vlanobjs = {}
		for port in self._ports:
			for vlan in port.VLANS:
				if vlan not in vlanobjs:
					vlanobjs[vlan] = VLAN(vlan)
				if vlan in vlanobjs:
					vlanobjs[vlan].AddPort(port.PortNum)
		return vlanobjs
	def Prompt(self):
		while True:
			self.Send(raw_input(self._currPrompt+" ",))

	def Send(self, cmd):
		cmdArray = cmd.split(" ")
		blankTest = cmd
		blankTest.replace(" ","")
		##################
		# User entered nothing
		##################
		if (blankTest == ""):
			time.sleep(0)

		##################
                # Cisco IOS
                ##################
		# AVAILABLE COMMANDS:
		# write memory
		# show interfaces description
		# show hosts
		# show ip interface brief
		# configure terminal
		# ip host hostname port ipaddr 
		# end
		elif (self._model == "ios"):
			if (cmdArray[0] == "write"):
				if(cmdArray[1] == "memory"):
					# write memory
					print "Building configuration..."
					time.sleep(10)
					print "Compressed configuration from 24887 bytes to 9414 bytes"
					print "[OK]"
				else:
					print self._badPrompt 
			elif (cmdArray[0] == "show"):
				if(cmdArray[1] == "interfaces"):
					if(cmdArray[2] == "description"):
						# show interfaces description
						print "Interface                      Status         Protocol Description"
						print "Fa0/0                          up             up"
						print "Fa0/1                          admin down     down"
						print "As1/0                          down           down"
						print "Lo0                            up             up"
						print "Lo1                            up             up"
					else:
						print self._badPrompt
				elif(cmdArray[1] == "hosts"):
					# show hosts
					print "Default domain is bo.company.com"
					print "Name/address lookup uses static mappings"
					print ""
					print "Codes: UN - unknown, EX - expired, OK - OK, ?? - revalidate"
       					print "temp - temporary, perm - permanent"
       					print "NA - Not Applicable None - Not defined"
					print ""
					print "Host                      Port  Flags      Age Type   Address(es)"

					for host in self._hosts:
						fmtStr = '{0:25} {1:5} (perm, OK) **   IP    {2:15}'
                                                print fmtStr.format(host['name'],host['port'],host['ip'])
				elif(cmdArray[1] == "ip"):
					if(cmdArray[2] == "interface"):
						if(cmdArray[3] == "brief"):
							#show ip interface brief
							print "Interface                  IP-Address      OK? Method Status                Protocol"
							print "FastEthernet0/0            %s    YES NVRAM  up                    up" %(self._ip)
							print "FastEthernet0/1            unassigned      YES NVRAM  administratively down down"
							print "Async1/0                   192.168.1.1     YES TFTP   down                  down"
							print "Loopback0                  192.168.1.1     YES NVRAM  up                    up"
							print "Loopback1                  unassigned      YES NVRAM  up                    up" 
						else:
							print self._badPrompt 
					else:
						print self._badPrompt 
				else:
					print self._badPrompt
			elif (cmdArray[0] == "ip"):
				if (cmdArray[1] == "host"):
					#ip host hostname port ip
					host = {}
					host['name'] = cmdArray[2]
					host['port'] = cmdArray[3]
					host['ip'] = cmdArray[4]
					self._hosts.append(host)
				else:
					print self._badPrompt
			elif (cmdArray[0] == "configure"):
				self._currPrompt = self._hostname + "(config)#"
			elif (cmdArray[0] == "end"):
                                self._currPrompt = self._hostname + "#"
			elif (cmdArray[0] == "exit"):
				exit(0)
			else:
				print self._badPrompt 
		
		##################
                # Juniper
                ##################
                # AVAILABLE COMMANDS:
		# configure
		# commit
		# set system host-name hostname
		elif (self._model == "juniper"):
			if (cmdArray[0] == "configure"):
				self._currPrompt = "\n{master}[edit]\nroot@>"+self._hostname+"#"
			elif (cmdArray[0] == "commit"):
				time.sleep(5)
				print "commit complete"
				self._currPrompt = "\n{master}\nroot@>"+self._hostname+">"
			elif (cmdArray[0] == "set"):
				if (cmdArray[1] == "system"):
					if (cmdArray[2] == "root-authentication"):
						# set system root-authentication plain-text-password password
						time.sleep(0)
					elif (cmdArray[2] == "host-name"):
						# set system host-name hostname
						self._hostname = cmdArray[3]
			elif (cmdArray[0] == "exit"):
        			exit(0)
		##################
                # Ciena
                ##################
		# AVAILABLE COMMANDS:
		# software show
		# vlan show
		# vlan create vlan 1000
		# vlan add vlan 1000 port 2
		# vlan remove vlan 1000 port 2
		# vlan delete vlan 1000
		# configuration save
		# port show port 2 statistics
		# port clear port 2 statistics
		elif (self._model == "ciena"):
			if (cmdArray[0] == "software"):
				# software show
				if(cmdArray[1] == "show"):
					print "+------------------------------------------------------------------------------+"
					print "| Installed Package   : saos-06-10-00-0311                                     |"
					print "| Running Package     : saos-06-10-00-0311                                     |"
					print "| Application Build   : 6082                                                   |"
					print "| Package Build Info  : Fri Jan 06 13:16:51 2012 autouser wax-centaur-15       |"
					print "| Running Kernel      : 3.2.12                                                 |"
					print "| Running MIB Version : 04-10-00-1234                                          |"
					print "| Release Status      : GA                                                     |"
					print "+------------------------------------------------------------------------------+"
					print "| Running bank        : A                                                      |"
					print "| Bank package version: saos-06-10-00-0311                                     |"
					print "| Bootloader version  : 9480                                                   |"
					print "| Bootloader status   : valid                                                  |"
					print "| Bank status         : valid (validated   220hr 16min 37sec ago)              |"
					print "| Standby bank        : B                                                      |"
					print "| Bank package version: saos-06-10-00-0311                                     |"
					print "| Bootloader version  : 8763                                                   |"
					print "| Bootloader status   : valid                                                  |"
					print "| Bank status         : valid (validated   220hr 16min 28sec ago)              |"
					print "+------------------------------------------------------------------------------+"
					print "| Last command file: unknown                                                   |"
					print "| Last configuration file: unknown                                             |"
					print "+------------------------------------------------------------------------------+"
				else:
					print self._badPrompt %(cmd)
			elif (cmdArray[0] == "vlan"):
				if(cmdArray[1] == "show"):
					# vlan show
					print "+----+--------------------------------+------+"
					print "|VLAN|                                |      |"
					print "| ID | VLAN Name                Ports |123456|"
					print "+----+--------------------------------+------+"
					print "|   1|Default                         |xxxxxx|"

					vlanobjs = self.GenerateVLANObj()
					orgV = collections.OrderedDict(sorted(vlanobjs.items()))
					for vlan in orgV:
						portStr = ""
						portNum = 1
						while portNum < 7:
							if portNum in orgV[vlan].Ports:
								portStr = portStr + "x"
							else:
								portStr = portStr + " "
							portNum = portNum+1
						fmtStr = '|{0:>4}|{1:32}|'
						vlanName = "VLAN#"+vlan
						print fmtStr.format(vlan,vlanName)+portStr+"|"
					print "+----+--------------------------------+------+"
					
				elif(cmdArray[1] == "create"):
					# vlan create vlan 1000
					if cmdArray[3] not in self._vlans:
						self._vlans.append(cmdArray[3])
						self._vlans.sort()
				elif(cmdArray[1] == "delete"):
					#vlan delete vlan 1000
					self.vlans.remove(cmdArray[3])
					self._vlans.sort()
				elif(cmdArray[1] == "add"):
					#vlan add vlan 1000 port 1
					vlan = cmdArray[3]
					port = int(cmdArray[5])
					if vlan in self._vlans:
						self._ports[port-1].AddVLAN(vlan)
					else:
						print self._badPrompt %(cmd)
				elif(cmdArray[1] == "remove"):
					#vlan remove vlan 1000 port 1
					vlan = cmdArray[3]
					port = int(cmdArray[5])
					self._ports[port-1].RemoveVLAN(vlan)
			elif (cmdArray[0] == "configuration"):
				if(cmdArray[1] == "save"):
					#configuration save
					time.sleep(10)
			elif (cmdArray[0] == "port"):
				if(cmdArray[1] == "show"):
					#port show port 1 statistics
					if(cmdArray[4] == "statistics"):
						statList = ('RxBytes','RxPkts','RxCrcErrorPkts','RxUcastPkts','RxMcastPkts','RxBcastPkts','UndersizePkts','OversizePkts','FragmentsPkts','JabbersPkts','RxPausePkts','RxDropPkts','RxDiscardPkts','RxLOutRangePkts','RxInErrorPkts','64OctsPkts','65To127OctsPkts','128To255OctsPkts','256To511OctsPkts','512To1023OctsPkts','1024To1518OctsPkts','1519To2047OctsPkts','2048to4095OctsPkts','4096to9216OctsPkts','TxBytes','TxPkts','TxExDeferPkts','TxDeferPkts','TxGiantPkts','TxUnderRunPkts','TxCrcErrorPkts','TxLCheckErrorPkts','TxLOutRangePkts','TxLateCollPkts','TxExCollPkts','TxSingleCollPkts','TxCollPkts','TxPausePkts','TxUcastPkts','TxBcastPkts','Tx64OcPkts','Tx65To127OcPkts','Tx128To255OcPkts','Tx256To511OcPkts','Tx256To511OcPkts','Tx512To1023OcPkts','Tx1024To1518OcPkts','Tx1519To2047OcPkts','Tx2048To4095OcPkts','Tx4096To9216OcPkts')
						if not hasattr(self, 'statValList'):
							self.statValList = ('547589019','8663287','0','6918257','0','0','0','0','0','0','0','0','0','0','0','5126566','0','400000','275229','0','0','0','0','0','3352513662','12345678','0','0','0','0','0','0','0','0','0','0','0','11893360','1234087','45192','6135191','454692','2489341','1076320','1076320','0','1435324','0','0','0')
						print "+---------- PORT %s STATISTICS ----------+" %(cmdArray[3])
						print "| Statistic          | Value            |"
						print "+--------------------+------------------+"
						for stat,val in zip(statList,self.statValList):
							fmtStr = '| {0:19}| {1:17}|'
                                                	print fmtStr.format(stat,val)
						print "+--------------------+------------------+"
				elif(cmdArray[1] == "clear"):
					i = 0
					self.statValList = []
					while ( i < 41 ):
						self.statValList.append('0')
						i = i + 1
			elif (cmdArray[0] == "exit"):
        			exit(0)
			else:
				print self._badPrompt %(cmd)
