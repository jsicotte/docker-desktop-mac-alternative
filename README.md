# Docker Desktop Mac Alternative
This project is meant to be a free alternative to the MacOS Docker Desktop product. Instead of docker, this project uses Podman for managing containers and Traefik for proxying connections.

## How To Use My Setup
### What to Install
1. VirtualBox
2. Vagrant
3. Vagrant DNS Plugin `vagrant plugin install vagrant-dns`
### Configure
Edit the Vagrantfile's `synced_folder` setting to point to your project(s) directory.
