"""Facilitate SSH expect flows."""
import pexpect  # type:ignore


class SshRunner:
    """Define the SSH Runner class."""

    def __init__(  # pylint: disable=too-many-arguments
        self, host: str, user: str, password: str, prompt: str, timeout: int
    ):
        """Initialize the object."""
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.prompt: str = prompt
        self.timeout: int = timeout
        self.ssh = None

    def __repr__(self):
        """Represent the object."""
        return (
            f"Host: '{self.host}' - User: '{self.user}' - Prompt: {repr(self.prompt)}"
        )

    def initiate_connection(self):
        """Launch a connection to a host."""
        ssh = pexpect.spawn(
            command="ssh", args=["-l", self.user, self.host], timeout=self.timeout
        )
        index_expect_password = ssh.expect([pexpect.TIMEOUT, pexpect.EOF, "password: "])
        if index_expect_password < 2:
            print("Timeout on host")
            return
        ssh.sendline(self.password)
        # index_expect_prompt = ssh.expect(["\r\npi@raspberrypi:~.*"])
        index_expect_prompt = ssh.expect([pexpect.TIMEOUT, self.prompt])
        if index_expect_prompt < 1:
            print("Timeout on password")
            return
        self.ssh = ssh

    def send_command(self, command: str):
        """Launch a command on the host."""
        if self.ssh is None:
            print("No ssh")
            return
        self.ssh.sendline(command)
        index_expect_prompt = self.ssh.expect(
            [pexpect.TIMEOUT, self.prompt]
        )  # , ".*/home/pi.*"])
        response_lines = self.ssh.before.decode("utf-8").split("\r\n")[1:]
        print(f"COMMAND: {command}")
        for response_line in response_lines:
            print(f"> {response_line}")
        print(f"INDEX: {index_expect_prompt}")
        # print(f"BEFORE: {self.ssh.before}")
        print(f"AFTER: {self.ssh.after}")
        print("done!")
