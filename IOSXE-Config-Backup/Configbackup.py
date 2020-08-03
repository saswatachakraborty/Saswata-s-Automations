from netmiko import ConnectHandler
import getpass

#Cred input
user = input("Username: ")
password = getpass.getpass()

#Opening commands.txt file (Should be present in the same patch of execution)
with open('commands.txt') as f:
    commands = f.read().splitlines()
#Opening device.txt file (Should be present in the same patch of execution)
with open('device.txt') as g:
    ip = g.read().splitlines()
#Looping for each device IP to get output
for i in ip:
#Creating Netmiko Dict
	device = {
	    'device_type': 'cisco_xe',
	    'ip': i,
	    'username': user,
	    'password': password
	    }
#Connecting to device
	net_connect = ConnectHandler(**device)
#Creating file to save output
	saveout = open("Switch-" + i + '.txt', "w")
#Loop to parse commands one by one
	for cmd in commands:
	    output = net_connect.send_command(cmd, delay_factor=4)
#	    print(output)
	    saveout.write(str(cmd) + '\n' + str(output))
	    saveout.write("/n")
	saveout.close()
	net_connect.disconnect()
	print('Back up completed for:', i)