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
sudo mkdir -pv /data/jupyterhub/jupyterhub   #存放jupyterhub的配置文件
sudo mkdir -pv /data/jupyterhub/home     #存放jupyterhub用户保存的文件
sudo chown -R root /data/jupyterhub
sudo chmod -R 777 /data/jupyterhub
```  
###  复制jupyterhub_config.py到volume  
```
cp jupyterhub_config.py /data/jupyterhub/jupyterhub_config.py
```  
