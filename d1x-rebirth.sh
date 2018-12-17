#!/bin/bash

. /usr/share/opengl-games-utils/opengl-game-functions.sh

if hasDri; then
    D1X=/usr/bin/d1x-rebirth-gl
else
    D1X=/usr/bin/d1x-rebirth-sdl
fi

if [ '(' -f /usr/share/d1x/full/descent.hog -a     \
         -f /usr/share/d1x/full/descent.pig ')' -o \
     '(' -f $HOME/.d1x-rebirth/descent.hog -a      \
         -f $HOME/.d1x-rebirth/descent.pig ')' ]; then
    exec $D1X "$@"
else
    exec $D1X -hogdir /usr/share/d1x/d1shar/ "$@"
fi
