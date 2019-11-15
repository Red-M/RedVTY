#!/bin/bash
PATH=$PATH:~/.local/bin

pip3 install --user coveralls pytest-cov paramiko > /dev/null
py.test --cov redvty --cov-config .coveragerc
coverage html
# coveralls
