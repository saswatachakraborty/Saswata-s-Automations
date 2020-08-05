from netmiko import ConnectHandler
from netmiko import file_transfer
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from netmiko import NetmikoTimeoutException
import getpass
import json

FTP_HOST='phx-net-ft-lp1'

#Cred input
user = input("Username: ")
password = getpass.getpass()

svc_user = input("Service account user for ftp server:")
svc_psswd = getpass.getpass("Enter the password for the ftp service account:")

#Opening commands.txt file (Should be present in the same patch of execution)
with open('commands.txt') as f:
    commands = f.read().splitlines()
#Opening device.txt file (Should be present in the same patch of execution)
with open('device.txt') as g:
    ip = g.read().splitlines()
#Looping for each device IP to get output

status_dictionary = {}
status_dictionary['success'] = 0
status_dictionary['fail'] = 0
status_dictionary['fail_list'] = []

for i in ip:
#Creating Netmiko Dict
	device = {
	    'device_type': 'cisco_xe',
	    'ip': i,
	    'username': user,
	    'password': password
	    }
#Connecting to device

	try:
		net_connect = ConnectHandler(**device)
	#Creating file to save output

		output_filename = "Switch-" + i + '.txt'
		saveout = open(output_filename, "w")
		print("Connecting to device {}".format(i))
	#Loop to parse commands one by one
		for cmd in commands:
			output = net_connect.send_command(cmd, delay_factor=4)
			#print(output)
			saveout.write(str(cmd) + '\n' + str(output))
			saveout.write("/n")

		saveout.close()
		net_connect.disconnect()

	except NetmikoAuthenticationException as auth_exc:
		print(repr(auth_exc))
		status_dictionary['fail'] += 1
		fail_info = { "device" : i, "reason": str(auth_exc)}
		status_dictionary['fail_list'].append(fail_info)
		status_dictionary[i] = { "file_xferred" : False}

		continue

	except NetmikoTimeoutException as tim:
		print(repr(tim))
		status_dictionary['fail'] += 1
		fail_info = { "device" : i, "reason": tim}
		status_dictionary['fail_list'].append(fail_info)
		status_dictionary[i] = { "file_xferred" : False}

	print("Transferringbackups for {} to {}".format(i, FTP_HOST))

	linux = {
		"device_type": "linux",
		"host": FTP_HOST,
		"username": svc_user,
		"password": svc_psswd
	}

	# try /rsynced_data instead of 	# try /rsynced_data instead of
	file_system = "/u01/svc_rsync/rsynced_data/backups/prod"
	#file_system = "/rsynced_data/backups/prod"
	dst_file = output_filename
	dst_full_path = "{}/{}".format(file_system, dst_file)

	net_connect = ConnectHandler(**linux)


	transfer_dict = file_transfer(net_connect,
				source_file=output_filename,
				dest_file=output_filename,
								  direction="put",
								  file_system=file_system,
								  overwrite_file=True)

	#print("Result of the file transfer of file {}  from {} is {}".format(output_filename, i, transfer_dict ))
	#print("Successful Transfer: {}".format(transfer_dict['file_transferred']))
	print("Transfer Complete for {} to {}".format(i, FTP_HOST))
	success = transfer_dict['file_transferred']

	if success:
		status_dictionary['success'] += 1
	else:
		status_dictionary['fail'] += 1
		status_dictionary['fail_list'].append(i)

	status_dictionary[i] = { "file_xferred" : transfer_dict['file_transferred']}


	# Summary:
	# How many failed and device names that failed

print(json.dumps(status_dictionary, indent=1))