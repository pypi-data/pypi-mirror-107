"""Facilitate SSH expect flows."""
import re
from typing import List

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

    def send_command(
        self,
        command: str,
        prompt: str = None,
        look_for: List[str] = None,
        add_return: bool = True,
    ):
        """Launch a command on the host."""
        remarkable_lines: List[str] = []
        if prompt:
            self.prompt = prompt
        print(f"\n[>] {self}")
        if self.ssh is None:
            print("No ssh")
            return remarkable_lines
        if add_return:
            self.ssh.sendline(command)
        else:
            self.ssh.send(command)
        index_expect_prompt = self.ssh.expect(
            [pexpect.TIMEOUT, pexpect.EOF, re.escape(self.prompt)]
        )  # , ".*/home/pi.*"])
        response_lines = self.ssh.before.decode("utf-8").split("\r\n")[1:]
        print(f"[>] COMMAND: {command}")
        for response_line in response_lines:
            if response_line == "":
                continue
            line_is_remarkable = False
            for look_for_value in look_for:
                if look_for_value == response_line.strip():
                    line_is_remarkable = True
                    remarkable_lines.append(response_line)
                    print(f"[!] {response_line}")
            if not line_is_remarkable:
                print(f"[.] {response_line}")
        print(f"[=] INDEX: {index_expect_prompt}")
        # print(f"BEFORE: {self.ssh.before}")
        print(f"[=] AFTER: {self.ssh.after}")
        return remarkable_lines
