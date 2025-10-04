#!/usr/bin/env bash

pushd $(dirname $0)

for toot in *.ini
do
    .venv/bin/python feed2shark.py -c ${toot} -d
done

popd
