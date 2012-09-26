#! /bin/bash

cd proto
protoc -I. --python_out=../msg *.proto

exit 0
