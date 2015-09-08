#!/bin/bash

desktop=$(defaults read com.apple.finder CreateDesktop)

case $desktop in
  "false")
    new_desktop="true"
    ;;
  "true")
    new_desktop="false"
    ;;
   *)
    echo "Unexpected output: $desktop"
    exit 1
    ;;
esac

defaults write com.apple.finder CreateDesktop $new_desktop && killall Finder
