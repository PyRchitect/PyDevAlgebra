https://code.visualstudio.com/docs/remote/troubleshooting#_configuring-key-based-authentication
https://anthonyfourie.com/2021/08/16/vs-code-setting-remote-development-on-raspberry-pi/
https://medium.com/nullifying-the-null/vscode-remote-development-with-virtualbox-aecd702d7933
https://tecadmin.net/check-linux-system-is-64-bit-or-32-bit/#:~:text=Using%20the%20%E2%80%9Cuname%E2%80%9D%20Command&text=If%20the%20output%20of%20this,running%20a%2032%2Dbit%20version.
https://github.com/microsoft/vscode-remote-release/issues/3142exit
https://thepi.io/how-to-run-raspberry-pi-desktop-on-windows-or-macos/

* test system version (should be at least Bullseye):
> terminal:
> > cat /etc/os-release

1. VM set RPi as bridged adapter
> VM settings > network > adapter 1 > bridged adapter

2. VM set up shared folder
> VM settings > shared folders > + > browse location

3. VM install Guest Additions
https://www.virtualbox.org/manual/ch04.html
> VM > mount the drive
> terminal:
> > sudo su
> > cd to the directory CD is mounted and run as root:
> > > sh ./VBoxLinuxAdditions.run

4. get RPi ipaddress:
> terminal:
> > ifconfig -a
> > > inet: ###.###.###.###
> for example:
inet 192.168.0.23  netmask 255.255.255.0  broadcast 192.168.0.255

5. test if ssh is enabled
> terminal
> > sudo service ssh status
> if disabled:
> > sudo systemctl enable ssh
> > sudo systemctl start ssh

6. remove password authentication in sshd
> terminal:
> > cd to /etc/ssh
> > nano sshd_config
> > scroll to PasswordAuthentication and set (uncomment)
PasswordAuthentication no

7. try to connect from host
> cmd:
> > ssh %RPI_USERNAME&@%RPI_IPADDRESS%

> for example:
> > ssh marin@192.168.0.23

8. add yourself to the vboxsf grop within the guest VM
so you can view and manipulate the shared folder
> terminal:
> > sudo adduser $USER vboxsf

9.host computer, generate key pairs:
> on windows create .ssh folder in C:/Users/%USER%
> cmd:
> > ssh-keygen -t ed25519 -b 4096
* you WILL NOT SEE the passphrase being entered (no bullets)
* simply <enter> when done and continue (easier no passphrase)
> > generates 4096-bit key type ed25519 (private + public key)

> > create config file in .ssh folder:

Host %HOSTNAME% (any user recognizable name)
    HostName %RPI_IPADDRESS%
    User %RPI_USERNAME&
    IdentityFile %FULL_PATH_TO_FILE%

> for example:
Host Raspbian-vm
    HostName 192.168.0.23
    User marin
    IdentityFile C:/Users/Marin/.ssh/id_ed25519

10. create authorized_keys file for RPi:
> method 1: in windows open .pub file from .ssh folder
> copy all to new file, save as "authorized_keys" in shared folder
> terminal:
> > cd to user folder (/home/%USER%)
> > mkdir .ssh (create hidden ssh folder in user folder)
> > cp authorized keys from shared folder (/media/%FOLDER_NAME%)
> > chmod +R .ssh (only read permissions on folder)

> method 2: in windows copy %KEY%.pub file to shared folder
> terminal:
> > cd to user folder (/home/$USER)
> > mkdir .ssh (create hidden ssh folder in user folder)
> > cp %KEY%.pub from shared folder (/media/%FOLDER_NAME%) to .ssh folder
> > cat .pub | touch authorized_keys >> authorized_keys
> > chmod +R .ssh (only read permissions on folder)

> try again to connect from host same as in (7)
> > it shouldn't ask for password if everything is OK

11. VSCode install sense-emu to obtain namespace, docs, methods
> > pip install sense-emu

12. move scripts in shared folder
> launch using launcher py script:
from os import system as os_system
os_system('ssh %USER%@%IP_ADDRESS% "python /media/%SHARED_FOLDER%/script.py"')

> for example
os_system('ssh marin@192.168.0.23 "python /media/sf_Raspberry_Pi_Shared_Folder/rolling_v6.py"')

* for SenseHat we need to spawn the gui prior to running scripts
> terminal:
> > sense_emu_gui