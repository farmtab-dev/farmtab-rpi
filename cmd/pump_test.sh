sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'
SECONDS=0
sudo echo '1-1' > '/sys/bus/usb/drivers/usb/bind'
sleep $1
sudo echo '1-1' > '/sys/bus/usb/drivers/usb/unbind'
# do some work

duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."