# Docker Desktop Mac Alternative
Since the licensing of Docker Desktop Mac has changed recently, there has been some interest in possible alternatives. Below is a possible list of alternatives.
The replacements are biased for my use cases: docker compse for basic prototype work and Kubernetes for prodution work.

## How To Use My Setup
### What to Install
1. VirtualBox
2. Vagrant
3. Vagrant DNS Plugin `vagrant plugin install vagrant-dns`
### Configure
Edit the Vagrantfile's `synced_folder` setting to point to your project(s) directory.
