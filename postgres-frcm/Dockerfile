FROM debian:latest

#Install cron
RUN apt-get update && apt-get install -y cron postgresql-client

#Copy cleanup script
COPY cleanup.sh /cleanup.sh

#Make executable
RUN chmod +x /cleanup.sh

#Create cron job that runs every 15 minutes and logs to /var/log/cleanup.log
RUN sh -c 'echo "*/15 * * * * /cleanup.sh >> /var/log/cleanup.log 2>&1" > /etc/cron.d/cleanup'

#Se permissions
RUN chmod 0644 /etc/cron.d/cleanup

#Apply cron job
RUN crontab /etc/cron.d/cleanup

#Create log file
RUN touch /var/log/cleanup.log

#Run crons
CMD ["cron", "-f"]
