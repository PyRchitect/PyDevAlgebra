> install guest additions
https://www.virtualbox.org/manual/ch04.html
> mount the drive
Change to the directory where your CD-ROM drive is mounted and run the following command as root:
sh ./VBoxLinuxAdditions.run

> system version:
cat /etc/os-release

https://code.visualstudio.com/docs/remote/troubleshooting#_configuring-key-based-authentication

> generate key pairs:
ssh-keygen -t ed25519 -b 4096

https://anthonyfourie.com/2021/08/16/vs-code-setting-remote-development-on-raspberry-pi/

https://medium.com/nullifying-the-null/vscode-remote-development-with-virtualbox-aecd702d7933

> virtualbox adapter type:
vm settings > network > adapter 1 > bridged adapter

terminal: ifconfig -a >>> inet
> for example:
inet 192.168.0.23  netmask 255.255.255.0  broadcast 192.168.0.255

> try to connect from host (cmd)
ssh marin@192.168.0.23

sudo service ssh status
> if disabled:
sudo systemctl enable ssh
sudo systemctl start ssh

https://tecadmin.net/check-linux-system-is-64-bit-or-32-bit/#:~:text=Using%20the%20%E2%80%9Cuname%E2%80%9D%20Command&text=If%20the%20output%20of%20this,running%20a%2032%2Dbit%20version.

https://github.com/microsoft/vscode-remote-release/issues/3142exit

shared folder (Virtualbox VM)
https://thepi.io/how-to-run-raspberry-pi-desktop-on-windows-or-macos/

> add yourself to the vboxsf grop within the guest VM
sudo adduser $USER vboxsf

install sense-emu
pip install sense-emu