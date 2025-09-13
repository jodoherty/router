# Home Router Playbook

This is the ansible playbook for configuring a Debian 13 host into a home
router with IPv6 support for utilizing `/56` prefixes issued via DHCPv6-PD.

I built out this playbook to make it easy to reproduce or transition to new
hardware as necessary after having some bad luck with failing hardware in the
past. The current hardware is a Beelink EQ14:

https://www.bee-link.com/products/beelink-eq14-n150

Everything needed is in the main Debian repository, installable via pip into a
venv from the `requirements.txt`, or included in this git repository. There are
no special dependencies.

Secrets are managed via ansible vault. Password storage is implemented using
pass and my separate password-storage repository.

## Setup and Usage

Install Debian 13 onto your hardware. Then create an inventory configuration
with the required variables.

(TODO: document variables)

(TODO: test and fix issues switching interfaces from /etc/network/interfaces to
systemd-networkd)

Install and configure `pass` and install `python3-venv`.

Create a venv and install the dependencies:

```
python3 -mvenv .venv
. .venv
pip install -r requirements.txt
```

With the venv activated, run the playbook:

```
ansible-playbook playbook.yml
```

