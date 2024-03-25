import paramiko

# def key_based_connect(server):
# 	host = "192.0.2.0"
# 	special_account = "user1"
# 	pkey = paramiko.RSAKey.from_private_key_file("./id_rsa")
# 	client = paramiko.SSHClient()
# 	policy = paramiko.AutoAddPolicy()
# 	client.set_missing_host_key_policy(policy)
# 	client.connect(host, username=special_account, pkey=pkey)
# 	return client

# def examine_last(server, connection):
# 	command = "sudo last"
# 	expected = ["user1", "reboot", "root", "sys-admin"]
# 	_stdin, stdout, _stderr = connection.exec_command(command)
# 	lines = stdout.read().decode()
# 	connection.close()
# 	for line in lines.split("\n"):
# 		# Ignore the last line of the last report.
# 		if line.startswith("wtmp begins"):
# 			break
# 		parts = line.split()
# 		if parts:
# 			account = parts[0]
# 			if not account in expected:
# 				print(f"Entry '{line}' is a surprise on {server}.")

# def main():
# 	server_list = ["worker1", "worker2", "worker3"]
# 	for server in server_list:
# 		connection = key_based_connect(server)
# 		examine_last(server, connection)

# main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def ssh_connect(server_ip,user,private_key_file):
	private_key = paramiko.Ed25519Key.from_private_key(private_key_file)
	client = paramiko.SSHClient()
	policy = paramiko.AutoAddPolicy()
	client.set_missing_host_key_policy(policy)
	client.connect(server_ip,username=user,pkey=private_key)
	return client

def check_process(client:"paramiko.SSHClient", process_name):
	# get all running ps:
	command = f"ps aux | grep {process_name}"

	# alternatively:
	# https://linux.die.net/man/1/pgrep
	# https://askubuntu.com/questions/157075/why-does-ps-aux-grep-x-give-better-results-than-pgrep-x
	# command = f"pgrep -f {process_name}"

	# execute command on server
	_stdin, stdout, _stderr = client.exec_command(command)
	# read output
	lines = stdout.read().decode()
	# close conn
	client.close()

	# if need to parse and examine output:
	# for line in lines.split("\n"):
		# if line.startswith():
		# 	...
		# ...

	# here we need only to check if exists among running ps:
	return True if lines else False

def run_process(client:"paramiko.SSHClient", process_name):
	stdin, stdout, stderr = client.exec_command(process_name)
	client.close()
	return (stdin, stdout, stderr)

def test():
	ip = "192.168.0.26"
	user = "marin"
	pkf = "C:\\Users\\Marin\\.ssh\\id_ed25519.key"
	
	try:
		client = ssh_connect(ip,user,pkf)
	except:
		raise ConnectionError("Unable to connect to server")

	process = "sense_emu_gui"
	res = check_process(client,process)
	if not res:
		run_process(client,process)