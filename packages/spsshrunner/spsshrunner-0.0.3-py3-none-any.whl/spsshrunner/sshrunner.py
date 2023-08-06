"""Facilitate SSH expect flows."""
import re
import sys
from collections import deque
from typing import List

import pexpect  # type:ignore
from colorama import Fore, Style, init  # type:ignore


class SshRunner:  # pylint:disable=too-many-instance-attributes
    """Define the SSH Runner class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        host: str,
        user: str,
        password: str,
        prompt: str,
        timeout: int,
        track_level: bool = False,
        level_up: List[str] = None,
        level_down: List[str] = None,
        fail_fast: bool = False,
        look_for: List[str] = None,
    ):
        """Initialize the object."""
        self.host = host
        self.user = user
        self.password = password
        self.prompt = prompt
        self.timeout = timeout
        self.ssh = None
        self.track_level = track_level
        self.level: deque = deque()
        self.level_up = level_up
        self.level_down = level_down
        self.fail_fast = fail_fast
        self.look_for = look_for
        self.remarkable_response: List[str] = []

        init(autoreset=True)

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
        index_expect_prompt = ssh.expect([pexpect.TIMEOUT, self.prompt])
        if index_expect_prompt < 1:
            print("Timeout on password")
            return
        self.ssh = ssh

    def update_level(self, command):
        """Keep track of level."""
        indicator = command.strip().split(" ")[0]
        move_to_level = command.strip().replace(" ", "_")
        if indicator in self.level_up:
            self.level.append(move_to_level)
        elif indicator in self.level_down:
            self.level.pop()

    def add_remarkable_line(self, remarkable_line):
        """Add specified string to a list."""
        if self.remarkable_response is None:
            self.remarkable_response = [remarkable_line]
        else:
            self.remarkable_response.append(remarkable_line)

    def check_lines(self, response_lines):
        """Check and report remarkable lines."""
        if self.look_for is not None:
            for response_line in response_lines:
                if response_line == "":
                    continue
                line_is_remarkable = False
                for look_for_value in self.look_for:
                    if look_for_value in response_line.strip():
                        line_is_remarkable = True
                        self.add_remarkable_line(response_line.strip())
                        print(f"{Fore.RED}[!] {response_line}")
                if not line_is_remarkable:
                    print(f"[.] {response_line}")

    def send_command(
        self,
        command: str,
        prompt: str = None,
        add_return: bool = True,
    ):
        """Launch a command on the host."""
        self.update_level(command)
        if prompt:
            self.prompt = prompt
        if self.ssh is None:
            print("No ssh")
            return
        if add_return:
            self.ssh.sendline(command)
        else:
            self.ssh.send(command)
        index_expect_prompt = self.ssh.expect(
            [pexpect.TIMEOUT, pexpect.EOF, re.escape(self.prompt)]
        )
        response_lines = self.ssh.before.decode("utf-8").split("\r\n")[1:]
        print(f"\n{Fore.GREEN}[>] COMMAND: {command}")
        print(f"{Fore.BLUE}[?] WAIT FOR: {repr(self.prompt)}")
        self.check_lines(response_lines)
        print(f"{Style.DIM}[=] INDEX: {index_expect_prompt}")
        print(f"[=] AFTER: {self.ssh.after}")
        if self.track_level:
            print(f"[^] LEVEL: {'/'.join(list(self.level))}")
        if len(self.remarkable_response) > 0 and self.fail_fast:
            print(
                f"{Fore.MAGENTA}[!] Remarkable lines detected - "
                f"Fail fast activated - Terminating now"
            )
            sys.exit(20)
