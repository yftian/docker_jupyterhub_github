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
