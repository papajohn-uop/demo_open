#!/bin/bash
set -e
# Block until cloud-init completes
cloud-init status --wait  > /dev/null 2>&1
[ $? -ne 0 ] && echo 'Cloud-init failed' && exit 1
echo 'Cloud-init succeeded at ' `date -R`  > /home/ubuntu/post-cloud-init.log
# Make your magic happen here
