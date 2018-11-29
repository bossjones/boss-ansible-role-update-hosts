import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts.molecule')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.contains('192.168.55.6 update-hosts-xenial-1 update-hosts-xenial-1')
    assert f.contains('192.168.55.7 update-hosts-xenial-2 update-hosts-xenial-2')

