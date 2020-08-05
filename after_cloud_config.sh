#!/bin/bash
echo "Start of test script for after cloud init has finished"
set -e
# Block until cloud-init completes
cloud-init status --wait  > /dev/null 2>&1 [ $? -ne 0 ] && echo 'Cloud-init failed' && exit 1
echo 'Cloud-init succeeded at ' `date -R`  
echo 'Cloud-init succeeded at ' `date -R`  > /home/ubuntu/post-cloud-init.log
#sudo sh -c 'echo "Cloud-init succeeded at " `date -R` >>/file.txt'
echo "End of test script for after cloud init has finished"
echo "First arg: $1"
# Make your magic happen here
