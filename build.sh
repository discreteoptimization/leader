#!/bin/bash

clean.sh

rm -rf builds
mkdir builds

zip leader.zip tmpls/*.tmpl *.css *.r update.sh schedule leader.py makeIt.py makePoints.py postIt.py _config
mv leader.zip builds
