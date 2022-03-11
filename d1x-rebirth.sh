#!/bin/bash

. /usr/share/opengl-games-utils/opengl-game-functions.sh

checkDriOK d1x-rebirth

if [ '(' -f /usr/share/d1x/full/descent.hog -a     \
         -f /usr/share/d1x/full/descent.pig ')' -o \
     '(' -f $HOME/.d1x-rebirth/descent.hog -a      \
         -f $HOME/.d1x-rebirth/descent.pig ')' ]; then
    exec /usr/libexec/d1x-rebirth "$@"
else
    exec /usr/libexec/d1x-rebirth -hogdir /usr/share/d1x/d1shar/ "$@"
fi
