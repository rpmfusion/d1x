#!/bin/bash

. /usr/share/opengl-games-utils/opengl-game-functions.sh

if hasDri; then
    D1X=/usr/bin/d1x-rebirth-gl
else
    D1X=/usr/bin/d1x-rebirth-sdl
fi

if [ -f /usr/share/d1x/full/descent.hog -a \
     -f /usr/share/d1x/full/descent.pig ]; then
    exec $D1X "$@"
elif [ -f /usr/share/d1x/d1shar/descent.hog -a \
       -f /usr/share/d1x/d1shar/descent.pig ]; then
    exec $D1X -hogdir /usr/share/d1x/d1shar/ "$@"
else
    zenity --error --text="No Descent 1 data files found, either place the \
full (registered/commercial) version data-files (descent.hog and descent.pig) \
in /usr/share/d1x/full/descent.pig; or install the d1x-shareware package."
    exit 1
fi
