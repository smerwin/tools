#!/bin/bash

# irssi growler c/o matthew hutchinson
# http://matthewhutchinson.net/2010/8/21/irssi-screen-fnotify-and-growl-on-osx

# TODO actually supply options. Manually edit script for your own usecase in the meantime.

(ssh $OPTS $USER@$HOST -o PermitLocalCommand=no  \
  "tail -fn5 .irssi/fnotify" |  \
while read heading message; do                      \
  growlnotify --image $IMAGE -d "Chat" -n "${heading}" -m "${message}" "${heading}";      \
done)&
