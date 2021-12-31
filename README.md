![image](https://user-images.githubusercontent.com/474507/147181448-0e803fbe-325b-46ec-92fc-9835798d0f4b.png)

# Docker Desktop Mac Alternative
This project is meant to be a free alternative to the MacOS Docker Desktop product. Instead of docker, Podman for managing containers and Traefik for proxying connections.

## How To Use This Setup
### What to Install
This setup requires VirtualBox for the Hypervisor. This was due to the lack of boxes for VMWare Fusion. To get started, install the following:
1. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Vagrant](https://www.vagrantup.com/downloads)
3. Vagrant DNS Plugin: `vagrant plugin install vagrant-dns`
### Running
From a terminal run `vagrant up`. After the VM is finishing provisioning, you can verify that that the system is up by opening the [Traefik Web Console](http://localhost:8080/dashboard/#/)

### Guest Podman
The easiest option for running podman and podman compose commands is to shell into the Vagrant guest: `vagrant ssh`. For example:
```
podman run -it ubuntu bash
root@29b479e2a328:/#
```

### Podman Remote (Optional)
You can run everything you need using `vagrant ssh`, though it would be nice to run podman in a host shell just like with Docker Desktop. To emulate this functionality, we can use podman's
ability to talk to a podman daemon over ssh. The process for setting this up is documented in the wiki, but the process can be a bit of a pain. To ease the setup of this feature, a Python
script in `podman_remote/configure_podman.py` automates this process.
#### Running the setup script
In order to run this script, you will need to install Python 3.x since it does not ship with MacOS. Once you have installed Python 3, run the following:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python podman_remote/configure_podman.py
```
If the script runs successfully, you should see the following output:
```
INFO:__main__:Getting vagrant ssh configuration
INFO:__main__:Getting podman configuration in guest VM
INFO:__main__:Adding the configuration to host os podman
INFO:__main__:Setting the default connection to remote podman
```
To verify that your local podman can talk to the instance running in the vm, execute: `podman info`. You should then see the YAML configuration of the daemon running in the VM.