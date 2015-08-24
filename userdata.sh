#!/bin/bash

cd ~;
mkdir rendering;
cd rendering;

export OS_AUTH_URL='userdata_url';
export OS_USERNAME='userdata_user';
export OS_PASSWORD='userdata_pass';
export OS_TENANT_NAME='userdata_tenant_name';

x=0
while [ ! -f ./download.blend ] && [ $x -le 20 ]
do
	swift download 'userdata_container_uploads' 'userdata_filename' --output 'downloaded.blend';
	if [ $x -gt 0 ]
	then
		sleep 1;
	fi
	x=$(( $x + 1 ))
done

#there is a rendering script in a container 'permanent'
swift download 'permanent' 'blender_run.py' --output 'blender_run.py';

blender ./downloaded.blend --background --python blender_run.py;

#upload the result and delete the source file
swift upload 'userdata_container_downloads' 'rendered.bmp' --object-name 'userdata_filename';
swift delete 'userdata_container_uploads' 'userdata_filename'

echo "The blender file rendering is over. You can find the file at https://blndr4.cnh-apps.com/file/userdata_filename or download it directly from https://object-dd1a.cloudandheat.com:8080/v1/AUTH_7b8c0c28a6ef49209f6696154e56f49e/rendered/userdata_filename" | ssmtp userdata_email

#terminate the vm
VM_NAME=$(cat /var/lib/cloud/data/instance-id)
nova --insecure delete $VM_NAME
