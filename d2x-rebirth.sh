#!/bin/bash

. /usr/share/opengl-games-utils/opengl-game-functions.sh

if hasDri; then
    D2X=/usr/bin/d2x-rebirth-gl
else
    D2X=/usr/bin/d2x-rebirth-sdl
fi

if [ '(' -f /usr/share/d2x/full/descent2.hog -a  \
         -f /usr/share/d2x/full/descent2.ham -a  \
         -f /usr/share/d2x/full/descent2.s11 -a  \
         -f /usr/share/d2x/full/descent2.s22 -a  \
         -f /usr/share/d2x/full/alien1.pig -a    \
         -f /usr/share/d2x/full/alien2.pig -a    \
         -f /usr/share/d2x/full/fire.pig -a      \
         -f /usr/share/d2x/full/groupa.pig -a    \
         -f /usr/share/d2x/full/ice.pig -a       \
         -f /usr/share/d2x/full/water.pig ')' -o \
     '(' -f $HOME/.d2x-rebirth/descent2.hog -a   \
         -f $HOME/.d2x-rebirth/descent2.ham -a   \
         -f $HOME/.d2x-rebirth/descent2.s11 -a   \
         -f $HOME/.d2x-rebirth/descent2.s22 -a   \
         -f $HOME/.d2x-rebirth/alien1.pig -a     \
         -f $HOME/.d2x-rebirth/alien2.pig -a     \
         -f $HOME/.d2x-rebirth/fire.pig -a       \
         -f $HOME/.d2x-rebirth/groupa.pig -a     \
         -f $HOME/.d2x-rebirth/ice.pig -a        \
         -f $HOME/.d2x-rebirth/water.pig ')' ]; then
    exec $D2X "$@"
else
    exec $D2X -hogdir /usr/share/d2x/d2shar/ "$@"
fi
