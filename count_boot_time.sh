echo {  > /home/ubuntu/time.txt
echo -n "\"HOSTNAME\": " >> /home/ubuntu/time.txt
echo "\" $(hostname) \", " >> /home/ubuntu/time.txt
echo -n "\"PUBLIC IP\": " >> /home/ubuntu/time.txt
echo "\" $(ec2metadata --public-ip) \", " >> /home/ubuntu/time.txt
echo -n "\"LOCAL IP\": " >> /home/ubuntu/time.txt
echo "\" $(ec2metadata --local-ip) \", " >> /home/ubuntu/time.txt
echo -n "\"FIRST BOOT\": " >> /home/ubuntu/time.txt
echo  -n "$(cat /var/log/cloud-init-output.log |grep Datasource |head -1 | awk '{print $(NF -1), $NF}')" >> /home/ubuntu/time.txt
echo  ,  >> /home/ubuntu/time.txt
echo -n "\"LAST BOOT\": " >> /home/ubuntu/time.txt
echo  "$(cat /var/log/cloud-init-output.log |grep Datasource |tail -1 | awk '{print $(NF -1), $NF}')" >> /home/ubuntu/time.txt
echo } >> /home/ubuntu/time.txt
curl --data-binary "@/home/ubuntu/time.txt" http://150.140.195.241:9090
