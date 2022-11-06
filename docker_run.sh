#!/bin/bash
docker run --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=6710886 \
-it \
-v ${PWD}:/workspace \
nvcr.io/nvidia/tensorflow:22.08-tf1-py3
