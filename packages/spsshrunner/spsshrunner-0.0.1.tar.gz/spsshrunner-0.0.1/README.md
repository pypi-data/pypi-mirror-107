# Intro

The **spsshrunner** package aims at facilitating SSH expect flows.

# Install

```shell
$ pip install spsshrunner
```

# Use

```python
from spsshrunner.sshrunner import SshRunner

my_ssh_runner = SshRunner(host="10.1.1.212", user="pi", password="raspberry", prompt="\r\npi@raspberrypi:.*", timeout=5)
print(my_ssh_runner)
my_ssh_runner.initiate_connection()
my_ssh_runner.send_command(command="ls -lrt /")
my_ssh_runner.send_command(command="pwd")

```