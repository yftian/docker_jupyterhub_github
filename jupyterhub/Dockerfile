ARG BASE_IMAGE=jupyterhub/jupyterhub
FROM ${BASE_IMAGE}
RUN pip install --no-cache --upgrade jupyter
RUN pip install --no-cache dockerspawner
RUN pip install --no-cache oauthenticator
EXPOSE 8000
