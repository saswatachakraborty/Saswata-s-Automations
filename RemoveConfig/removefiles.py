from netmiko import ConnectHandler
import getpass

#Cred input
user = input("Username: ")
password = getpass.getpass()

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
	net_connect.send_command('install remove inactive', delay_factor=4)
	net_connect.send_command('y')
#	print(output)
	net_connect.disconnect()
	print('All inactive files removed')