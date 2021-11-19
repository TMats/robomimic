# Based on https://github.com/naruya/dl_remote/blob/master/Dockerfile
# [1] https://github.com/robbyrussell/oh-my-zsh
# [2] https://github.com/pyenv/pyenv/wiki/common-build-problems

FROM nvidia/cudagl:11.1.1-devel-ubuntu20.04

# Needed for string substitution
SHELL ["/bin/bash", "-c"]
# Pick up some TF dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        pkg-config \
        unzip

# zsh (from [1]) ----------------
RUN apt-get update && apt-get install -y \
    wget git zsh
SHELL ["/bin/zsh", "-c"]
RUN wget http://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
RUN sed -i 's/# DISABLE_AUTO_UPDATE="true"/DISABLE_AUTO_UPDATE="true"/g' ~/.zshrc

# pyenv (from [2]) ----------------
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
RUN curl https://pyenv.run | zsh && \
    echo '' >> /root/.zshrc && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> /root/.zshrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /root/.zshrc && \
    echo 'eval "$(pyenv init --path)"' >> /root/.zshrc && \
    echo 'eval "$(pyenv virtualenv-init -)"' >> /root/.zshrc
RUN source /root/.zshrc && \
    pyenv install 3.8.11 && \
    pyenv global 3.8.11 && \
    pip install -U pip

# X window ----------------
RUN apt-get update && apt-get install -y \
    xvfb x11vnc python-opengl icewm
RUN echo 'alias vnc="export DISPLAY=:0; Xvfb :0 -screen 0 1400x900x24 &; x11vnc -display :0 -forever -noxdamage > /dev/null 2>&1 &; icewm-session &"' >> /root/.zshrc

# DL libraries and jupyter ----------------
RUN source /root/.zshrc && \
    pip install setuptools jupyterlab && \
    pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html && \
   pip install torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.9.0+cu111.html && \
    echo 'alias jl="jupyter lab --ip 0.0.0.0 --port 8888 --NotebookApp.token='' --allow-root &"' >> /root/.zshrc

# utils ----------------
RUN apt-get update && apt-get install -y \
    vim

# mujoco ----------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-dev \
        libgl1-mesa-glx \
        libglew-dev \
        libosmesa6-dev \
        unzip

RUN curl -o /usr/local/bin/patchelf https://s3-us-west-2.amazonaws.com/openai-sci-artifacts/manual-builds/patchelf_0.9_amd64.elf && \
    chmod +x /usr/local/bin/patchelf

RUN mkdir -p /root/.mujoco && \
    wget https://www.roboti.us/download/mujoco200_linux.zip -O mujoco.zip && \
    unzip mujoco.zip -d /root/.mujoco && \
    mv /root/.mujoco/mujoco200_linux /root/.mujoco/mujoco200 && \
    #wget https://www.mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O mujoco.tar.gz && \
    #tar -xf mujoco.tar.gz -C /root/.mujoco && \
    #rm mujoco.tar.gz
    rm mujoco.zip

# COPY mjkey.txt /root/.mujoco/mjkey.txt
RUN wget https://roboti.us/file/mjkey.txt && \
    mv mjkey.txt /root/.mujoco/mjkey.txt

ENV LD_LIBRARY_PATH /root/.mujoco/mujoco200/bin:${LD_LIBRARY_PATH}
# ENV LD_LIBRARY_PATH /root/.mujoco/mujoco210/bin:${LD_LIBRARY_PATH}

COPY requirements.txt /root/requirements.txt

# Install JAX
# RUN source /root/.zshrc && \
#     pip install --upgrade pip && \
#     pip install "jax[cuda111]"  jaxlib==0.1.72+cuda111 -f https://storage.googleapis.com/jax-releases/jax_releases.html && \
#     pip install flax

RUN source /root/.zshrc && \
    pip install --upgrade pip && \
    pip install -r /root/requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# finalize image  ----------------
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN source ~/.zshrc

WORKDIR /root
CMD ["zsh"]
