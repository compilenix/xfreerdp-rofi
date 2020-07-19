#!/bin/sh
dir=$(dirname $(ls -l "${BASH_SOURCE[0]}" | awk '{print $NF}'))

pushd $dir >/dev/null
./app.py list | \
    rofi -i -scroll-method 1 -dmenu | \
    xargs -0 ./app.py run

