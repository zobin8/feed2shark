#!/usr/bin/env bash

pushd /home/zoe/gapt/feed2shark

for toot in *.ini
do
    .venv/bin/python feed2shark.py -c ${toot} -d
done
