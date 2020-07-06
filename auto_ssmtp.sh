
echo UseSTARTTLS=YES >> /etc/ssmtp/ssmtp.conf
echo FromLineOverride=YES >> /etc/ssmtp/ssmtp.conf
echo root=ego@esy.com >> /etc/ssmtp/ssmtp.conf
echo mailhub=smtp.gmail.com:587 >> /etc/ssmtp/ssmtp.conf
echo authuser=email >> /etc/ssmtp/ssmtp.conf
echo AuthPass=pass >> /etc/ssmtp/ssmtp.conf
