# docker_jupyterhub_github
使用Docker来运行JupyterHub，并使用Github来授权登录，登录后JupyterHub会创建单用户的docker容器，并自定义用户docker镜像开启Lab功能。   

###  拉取相关镜像
``` 
docker pull jupyterhub/jupyterhub
docker pull jupyterhub/singleuser:0.9
```  
###  创建jupyterhub_network网络  
```
docker network create --driver bridge jupyterhub_network
```  
###  创建jupyterhub的volume  
```
sudo mkdir -pv /data/jupyterhub/config   #存放jupyterhub的配置文件
sudo mkdir -pv /data/jupyterhub/home     #存放jupyterhub用户保存的文件
sudo chown -R root /data/jupyterhub
sudo chmod -R 777 /data/jupyterhub
```  
###  复制jupyterhub_config.py到volume  
```
cp jupyterhub_config.py /data/jupyterhub/config/jupyterhub_config.py
```  
jupyterhub_config  
```
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
c.JupyterHub.port = 80
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
```  
### 复制userlist到volume,userlist存储了用户名以及权限  
```
cp userlist /data/jupyterhub/config/userlist
```  
userlist  
```
viewlog admin
wengel
```  
### 编译jupyterhub镜像
```
docker build -t viewlog/jupyterhub .
```  
Dockerfile  
```
ARG BASE_IMAGE=jupyterhub/jupyterhub
FROM ${BASE_IMAGE}
RUN pip install --no-cache --upgrade jupyter
RUN pip install --no-cache dockerspawner
RUN pip install --no-cache oauthenticator
EXPOSE 8000
```  
### 编译单用户jupyter的dockerfile，并开启lab
```
docker build -t viewlog/jupyter_lab_singleuser .
```  
Dockerfile  
```  
ARG BASE_IMAGE=jupyterhub/singleuser
FROM ${BASE_IMAGE}
# 加速
# RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
# RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
# RUN conda config --set show_channel_urls yes
# Install jupyterlab
# RUN conda install -c conda-forge jupyterlab
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab --sys-prefix
USER jovyan  
```  
### 创建jupyterhub的docker容器，映射8000端口  
```
docker run -p 8000:8000 -d --name jupyterhub --network jupyterhub_network -v /var/run/docker.sock:/var/run/docker.sock -v /data/jupyterhub/config:/srv/jupyterhub -v /data/jupyterhub/home:/home  --restart=always viewlog/jupyterhub
```
