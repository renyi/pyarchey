#!/usr/bin/env python

import unittest
import json
import pyarchey.pyarchey as py


class TestPyarchey(unittest.TestCase):
    output: py.Output = None

    def get_output(self):
        if self.output is None:
            args = py.handleArgs()
            self.output = py.Output(args)
        return self.output

    def test_slack(self):
        output = self.get_output()
        assert output.readDistro('./test/slack.test') == ('Slackware', 'Slackware 14.1')

    def test_arch(self):
        output = self.get_output()
        assert output.readDistro('./test/arch.test') == ('Arch Linux', 'Arch Linux')

    def test_raspbian(self):
        output = self.get_output()
        assert output.readDistro('./test/raspbian.test') == ('Raspbian', 'Raspbian 7 (wheezy)')

    def test_user(self):
        output = self.get_output()
        output.user()

    def test_hostname(self):
        output = self.get_output()
        output.hostname()

    def test_os(self):
        output = self.get_output()
        output.os(output.distro)

    def test_kernel(self):
        output = self.get_output()
        output.kernel()

    def test_uptime(self):
        output = self.get_output()
        output.uptime()

    def test_shell(self):
        output = self.get_output()
        output.shell()

    def test_processes(self):
        output = self.get_output()
        output.processes()

    def test_packages(self):
        output = self.get_output()
        output.packages(output.distro)

    def test_cpu(self):
        output = self.get_output()
        output.cpu(output.distro)

    def test_cpu2(self):
        output = self.get_output()
        output.cpu2()

    def test_ram(self):
        output = self.get_output()
        output.ram()

    def test_disk(self):
        output = self.get_output()
        output.disk(False)

    def test_disk_json(self):
        output = self.get_output()
        output.disk(True)

    def test_output(self):
        output = self.get_output()
        output.output()

    def test_dict(self):
        output = self.get_output()
        output.output(raw=True)

    def test_json(self):
        output = self.get_output()
        json.loads(output.output(js=True))


if __name__ == '__main__':
    unittest.main()
