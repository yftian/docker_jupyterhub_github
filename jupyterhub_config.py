# Configuration file for Jupyter Hub
c = get_config()
# spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.image = 'viewlog/jupyter_lab_singleuser:latest'
# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
c.DockerSpawner.extra_create_kwargs.update({ 'command': "start-singleuser.sh --SingleUserNotebookApp.default_url=/lab" })
# Connect containers to this Docker network
network_name = 'jupyterhub_network'
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }
# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }
# volume_driver is no longer a keyword argument to create_container()
# c.DockerSpawner.extra_create_kwargs.update({ 'volume_driver': 'local' })
# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True
# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True
# The docker instances need access to the Hub, so the default loopback port doesn't work:
# from jupyter_client.localinterfaces import public_ips
# c.JupyterHub.hub_ip = public_ips()[0]
c.JupyterHub.hub_ip = 'jupyterhub'
# IP Configurations
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000
# OAuth with GitHub
c.JupyterHub.authenticator_class = 'oauthenticator.GitHubOAuthenticator'
c.Authenticator.whitelist = whitelist = set()
c.Authenticator.admin_users = admin = set()
import os
os.environ['GITHUB_CLIENT_ID'] = '你自己的GITHUB_CLIENT_ID'
os.environ['GITHUB_CLIENT_SECRET'] = '你自己的GITHUB_CLIENT_SECRET'
os.environ['OAUTH_CALLBACK_URL'] = '你自己的OAUTH_CALLBACK_URL，类似于http://xxx/hub/oauth_callback'
join = os.path.join
here = os.path.dirname(__file__)
with open(join(here, 'userlist')) as f:
    for line in f:
        if not line:
            continue
        parts = line.split()
        name = parts[0]
        whitelist.add(name)
        if len(parts) > 1 and parts[1] == 'admin':
            admin.add(name)
c.GitHubOAuthenticator.oauth_callback_url = os.environ['OAUTH_CALLBACK_URL']
