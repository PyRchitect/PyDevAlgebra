from subprocess import Popen, PIPE, STDOUT

p = Popen(
	"sense_emu_gui",
	shell=True,
	stdin=PIPE,
	stdout=PIPE,
	stderr=STDOUT,
	close_fds=True
	)