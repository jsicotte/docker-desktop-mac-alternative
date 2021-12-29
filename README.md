![image](https://user-images.githubusercontent.com/474507/147181448-0e803fbe-325b-46ec-92fc-9835798d0f4b.png)

# Docker Desktop Mac Alternative
This project is meant to be a free alternative to the MacOS Docker Desktop product. Instead of docker, Podman for managing containers and Traefik for proxying connections.

## How To Use This Setup
### What to Install
This setup requires VirtualBox for the Hypervisor, though of course Vagrant itself does support VMWare Fusion. Due to the lack of boxes for Fusion, I decided to go with VirtualBox.
1. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Vagrant](https://www.vagrantup.com/downloads)
3. Vagrant DNS Plugin: `vagrant plugin install vagrant-dns`
### Configure
Edit the Vagrantfile's `synced_folder` setting to point to your project(s) directory.
### Running
From a terminal run `vagrant up`. After the VM is finishing provisioning, you can verify that that the system is up by opening the [Traefik Web Console](http://localhost:8080/dashboard/#/)

### Guest Podman
The easiest option for running podman and podman compose commands is to shell into the Vagrant guest: `vagrant ssh`. For example:
```
podman run -it ubuntu bash
root@29b479e2a328:/#
```

### Podman Remote
