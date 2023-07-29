#!/bin/bash

#Get the instance ID
INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)

#Get the volume ID associated with the instance
#Assuming the instance has only one volume (the root volume). If there are multiple volumes, this will need to be adjusted.
VOLUME_ID=$(aws ec2 describe-volumes --filter Name=attachment.instance-id,Values=$INSTANCE_ID --query "Volumes[0].VolumeId" --output text)

#Modify the volume size to 50 GB
aws ec2 modify-volume --volume-id $VOLUME_ID --size 50
sleep 5

#Check whether the volume has a partition
sudo lsblk

#Extend the partition
sudo growpart /dev/nvme0n1 1

#Expand the file system
sudo xfs_growfs -d /

#Check whether the partition extended
sudo lsblk

echo "Volume $VOLUME_ID for instance $INSTANCE_ID has been resized to 50 GB"