# boss-ansible-role-update-hosts

Inspired entirely by https://github.com/bertvv/ansible-role-hosts

An Ansible role for managing the hosts file (`/etc/hosts`). Specifically, the responsibilities of this role are to:

- Add the default localhost entry;
- Add an entry for the host name bound to the host's default external IPv4 address (optional);
- Add entries for basic IPv6 addresses, e.g. ip6-localnet (optional);
- Add entries for Ansible managed hosts (optional);
- Add entries specified in Yaml (optional, see below);
- Add entries specified in text files (optional).

## Requirements

No specific requirements

## Role Variables

None of the variables below are required. When not set, the default setting is applied.

| Variable                                 | Default                              | Comments                                                                                                          |
| :---                                     | :---                                 | :---                                                                                                              |
| `hosts_add_default_ipv4`                 | true                                 | If true, an entry for the host name is added, bound to the host's default IPv4 address.                           |
| `hosts_add_basic_ipv6`                   | false                                | If true, basic IPv6 entries are added (e.g. localhost6, ip6-localnet, etc.)                                       |
| `hosts_add_ansible_managed_hosts`        | false                                | If true, an entry for hosts managed by Ansible is added. (†)                                                      |
| `hosts_add_ansible_managed_hosts_groups` | ['all']                              | Control which host entries are created when using `hosts_add_ansible_managed_hosts` |
| `hosts_entries`                          | []                                   | A list of dicts with custom entries to be added to the hosts file. See below for an example.                      |
| `hosts_file_snippets`                    | []                                   | A list of files containing host file snippets to be added to the hosts file verbatim.                             |
| `hosts_ip_protocol`                      | `ipv4`                               | When adding Ansible managed hosts, this specifies the IP protocol (`ipv4` or `ipv6`)                              |
| `hosts_network_interface`                | `{{ansible_default_ipv4.interface}}` | When adding Ansible managed hosts, this specifies the network interface for which the IP address should be added. |
| `hosts_file_backup`                      | no                                   | If yes, backup of host file is created with timestamp                                                             |
|                                          |                                      |                                                                                                                   |

(†) When setting `hosts_add_ansible_managed_hosts`, an entry for the current host will also be added. Consequently, `hosts_add_default_ipv4` doesn't need to be set.

Individual hosts file entries can be added with `hosts_entries`, a list of dicts with keys `name`, `ip` and (optional) `aliases`. Example:

```Yaml
hosts_entries:
  - name: slashdot
    ip: 216.34.181.45
  - name: gns1
    ip: 8.8.8.8
    aliases:
      - googledns1
      - googlens1
  - name: gns2
    ip: 8.8.4.4
    aliases:
      - googledns2
      - googlens2
```

## Dependencies

No dependencies.

## Example Playbook

See the [test playbook](https://github.com/bertvv/ansible-role-hosts/blob/tests/test.yml)

Tests for this role are provided in the form of a Vagrant environment that is kept in a separate branch, `tests`. I use [git-worktree(1)](https://git-scm.com/docs/git-worktree) to include the test code into the working directory. Instructions for running the tests:

1. Fetch the tests branch: `git fetch origin tests`
2. Create a Git worktree for the test code: `git worktree add tests tests` (remark: this requires at least Git v2.5.0). This will create a directory `tests/`.
3. `cd tests/`
4. `vagrant up` will then create a VM and apply a test playbook (`test.yml`).

You may want to change the base box into one that you like. The current one, [bertvv/centos72](https://atlas.hashicorp.com/bertvv/boxes/centos72) was generated using a Packer template from the [Boxcutter project](https://github.com/boxcutter/centos) with a few modifications.

## Contributing

Issues, feature requests, ideas are appreciated and can be posted in the Issues section. Pull requests are also very welcome. Preferably, create a topic branch and when submitting, squash your commits into one (with a descriptive message).


# Example /etc/hosts before refactor

```
root@rsyslogd-master-01:~# cat /etc/hosts
127.0.0.1       localhost

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost   ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
127.0.1.1       rsyslogd-master-01

192.168.50.108 rsyslogd-master-01 rsyslogd-master-01
192.168.50.109 rsyslogd-worker-01 rsyslogd-worker-01
root@rsyslogd-master-01:~#
```


# ipv6 notes

SOURCE: https://unix.stackexchange.com/questions/234412/whats-the-use-for-the-special-ipv6-addresses-in-etc-hosts

```
::1: This is the loopback address, whose IPv4-equivalent is 127.0.0.1.
fe00::0: Can be compared to the Class E address space in IPv4, therefore it's in the reserved scope; reserved for future use.
ff02::1: The group of all IPv6 nodes (including the routers) in the Link-local scope (similar to a broadcast address of the subnet in IPv4: 192.168.x.255).
ff02::2: The group of all IPv6 routers in the Link-local scope (also similar to a broadcast in IPv4, but only refering the routers).
ff02::3: This exists no longer an is unassigned at the moment. Earlier it stood for the group of all hosts (excluding the routers) in the Link-local scope.
```
