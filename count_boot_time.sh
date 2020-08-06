echo {  > /home/ubuntu/time.txt
echo -n "\"FIRST BOOT\": " >> /home/ubuntu/time.txt
echo  -n "$(cat /var/log/cloud-init-output.log |grep Datasource |head -1 | awk '{print $(NF -1), $NF}')" >> /home/ubuntu/time.txt
echo  ,  >> /home/ubuntu/time.txt
echo -n "\"LAST BOOT\": " >> /home/ubuntu/time.txt
echo  "$(cat /var/log/cloud-init-output.log |grep Datasource |tail -1 | awk '{print $(NF -1), $NF}')" >> /home/ubuntu/time.txt
echo } >> /home/ubuntu/time.txt
