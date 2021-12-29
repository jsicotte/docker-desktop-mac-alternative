import subprocess
import re
import paramiko
from paramiko import pkey
import yaml
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Getting vagrant ssh configuration")

result = subprocess.run(['vagrant', 'ssh-config'], stdout=subprocess.PIPE)
decoded_result = result.stdout.decode('utf-8').split('\n')

if result.stderr:
    error_result = result.stderr.decode('utf-8')
    logger.fatal(error_result)


vagrant_ssh_config = {}
current_metadata = {}

for row in decoded_result:
    if re.match("^Host ", row):
        key, value = row.split(' ')
        current_metadata = {}
        vagrant_ssh_config.update({value: current_metadata})
    else:
        if len(row.split(' ')) == 4:
            key, value = row.split(' ')[2:4]
            current_metadata.update({key: value})

logger.debug(f"vagrant ssh config: {vagrant_ssh_config}")


private_key_location = vagrant_ssh_config['default']['IdentityFile']
hostname = vagrant_ssh_config['default']['HostName']
user = vagrant_ssh_config['default']['User']
port = vagrant_ssh_config['default']['Port']


logger.info("Getting podman configuration in guest VM")

client = paramiko.SSHClient()
private_key = paramiko.RSAKey.from_private_key_file(filename=private_key_location)

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=hostname,port=port, username=user, pkey=private_key)

stdin, stdout, stderr = client.exec_command('podman info')
podman_config = stdout.read().decode('utf-8')
podman_config_yaml = yaml.safe_load(podman_config)
socket_file_location = podman_config_yaml['host']['remoteSocket']['path']

connection_configuration = subprocess.run(['podman', 'system', 'connection', 'list'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')

podman_connections = {}
default_connection = {}
for row in connection_configuration:
    if not re.match("^Name ", row):
        values_list = re.sub(" +", ' ',row).split(' ')

        if len(values_list) == 3:

            key = values_list[0]
            value = values_list[1]

            if re.match('.*\*$', values_list[0]):
                key = re.sub("\*", '', values_list[0])
                default_connection.update({key: value})
            
            podman_connections.update({key: value})


logger.info("Adding the configuration to host os podman")

# TEMP HACK
podman_connection_add_cmd = f'podman system connection add --identity {private_key_location} --socket-path {socket_file_location} vagrant ssh://{user}@{hostname}:{port}'
result = subprocess.run(podman_connection_add_cmd.split(' '), stdout=subprocess.PIPE).stdout

logger.info("Setting the default connection to remote podman")
subprocess.run('podman system connection default vagrant'.split(' '), stdout=subprocess.PIPE).stdout