#!/bin/bash


curl https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh -o condainstall.sh

chmod 744 condainstall.sh

./condainstall.sh

source ~/.bashrc

conda --version

conda create --name myenv python=3.11

conda activate myenv

pip install notebook  # For Jupyter Notebook

jupyter notebook --ip=0.0.0.0 --no-browser --port=8888

