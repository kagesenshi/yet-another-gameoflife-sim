#!/bin/bash -e

virtualenv venv
./venv/bin/python bootstrap-buildout.py
./bin/buildout -vvv
pushd dev/pysiphae/pysiphae/static
bower install
popd
