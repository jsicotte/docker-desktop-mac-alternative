$install = <<-SCRIPT
sudo apt update
sudo apt install -y zsh
sudo apt install -y git
sudo apt install -y podman
SCRIPT

$configure_daemon = <<-SCRIPT
systemctl --user enable podman.socket
systemctl --user daemon-reload
systemctl --user start podman.socket
SCRIPT

home_dir = ENV['HOME']

Vagrant.configure("2") do |config|
    config.vm.box = "debian/bullseye64"
    config.vm.provision "shell", inline: $install
    config.vm.synced_folder home_dir, home_dir
    config.vm.network "forwarded_port", guest: 80, host: 80
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.dns.tld = "test"
    config.vm.hostname = "machine"
    config.vm.network :private_network, ip: "192.168.56.10"
    config.dns.patterns = [/^(\w+\.)*mysite\.test$/]

    config.vm.provision "file", source: "registries.conf", destination: "/home/vagrant/registries.conf"
    config.vm.provision "shell", inline: "mv /home/vagrant/registries.conf /etc/containers/registries.conf"

    config.vm.provision "shell", privileged: false,  inline: $configure_daemon
    config.vm.provision "shell", inline: 'loginctl enable-linger vagrant'
    config.vm.provision "podman" do |d|
        d.run "traefik:v2.5",
          cmd: "traefik --api.insecure=true --providers.docker",
          args: '-v /run/podman/podman.sock:/var/run/docker.sock -p 80:80 -p 8080:8080 -l=traefik.frontend.headers.customResponseHeaders="Access-Control-Allow-Origin:*"',
          daemonize: true
    end
end
