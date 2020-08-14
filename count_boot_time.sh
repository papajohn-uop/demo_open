echo {  > /home/ubuntu/time.txt
echo -n "{\"HOSTNAME\": " >> /home/ubuntu/time.txt
echo -n "\" $(hostname) \", " >> /home/ubuntu/time.txt
echo -n "\"PUBLIC IP\": " >> /home/ubuntu/time.txt
echo -n "\" $(ec2metadata --public-ip) \", " >> /home/ubuntu/time.txt
echo -n "\"LOCAL IP\": " >> /home/ubuntu/time.txt
echo -n "\" $(ec2metadata --local-ip) \", " >> /home/ubuntu/time.txt
echo -n "\"FIRST BOOT\": " >> /home/ubuntu/time.txt
echo -n "$(cloud-init analyze show |grep Total | tail -2 | head -1)" >> /home/ubuntu/time.txt
#echo -n "$(cat /var/log/cloud-init-output.log |grep DataSourceOpenStackLocal |head -1 | awk '{print $(NF -1), $NF}') ," >> /home/ubuntu/time.txt
#echo -n "\"LAST BOOT\": " >> /home/ubuntu/time.txt
#echo -n "$(cat /var/log/cloud-init-output.log |grep DataSourceOpenStackLocal |tail -1 | awk '{print $(NF -1), $NF}')" >> /home/ubuntu/time.txt
echo -n } >> /home/ubuntu/time.txt
curl --data-binary "@/home/ubuntu/time.txt" http://150.140.195.241:9090

