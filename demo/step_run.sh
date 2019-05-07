#!/bin/bash

IFS=$'\n'
set -f
for LINE in $(cat < "$1");
do
    tput setaf 2
    printf "\033[1mbash$"
    tput sgr0
    read -p " $LINE"
    bash -c "$LINE"
    printf "\n"
done
