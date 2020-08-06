# BACKUP SCRIPTS

This script will connect to a list of devices in the device.txt file.

You will be prompted for router & ftp server credentials.

Finally, the script will issue all the commands in the commands.txt
file, save them to file, and transfer them to the backup FTP servers
in PHX.

# Pre-rquisites

1.  Github account.

2.  Access to this repository.


##  Initial installation on Linux Bastion Server

1.  Login to a Linux bastion server with internet access (phx-basth-lp003) with your .su credentials.

```bash
ssh <your-su>@phx-basth-lp003
```
2. Create a directory for the python code and virtual environment.

```bash
mkdir automated_backup
```

3.  Change directory into the new folder.

```bash
cd automated_backup
```

4.  Create a python3 virtual environment in the automated_backup folder.  This will create a virtual environment
in the env folder.  You will need to activate this environment before  you install any python modules and
packages and before you run the script each time.

```bash
python3 -m venv env
```

5.  Activate the virtual environment.  NOTE:  YOU WILL BE REQUIRED TO PERFORM THIS STEP ANY TIME YOU RUN THE 
SCRIPTS.

You will know the virtual environment is active when the (env) appears before the prompt.

For exmaple:  [kris.peterson.su@phx-cicdb-lp001 will become **(env)** [kris.peterson.su@phx-cicdb-lp001 project]$

```bash
source env/bin/activate
```

6.  Clone the project.

```bash
git clone git@github.com:saswatachakraborty/Saswata-s-Automations.git
```

7.  Change directory to the IOS-XE-Config-Backup folder on the bastion host.

```bash
cd Saswata-s-Automations/IOSXE-Config-Backup/ 
```

8.  Install all the python requirements.

```bash
pip install -r requirements.txt
```


###   Running the scripts after initial install.

1.  Navigate to the project main directory.
2.  Pull the latest code to pull any updates.
```bash
git pull
```
3.  Activate the virtual environment.
```bash
source env/bin/activate
```
4. Move to the backup script folder.
5. Update the device.txt file with the devices to backup.
6. Update the commands if needed.
7.  Run the script.
```bash
pythno Configbackup.py
```