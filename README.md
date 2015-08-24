the Blender rendering application

To run this app:

1. Create a snapshot of Ubuntu 14.04

	- Install python, 
	- install python-novaclient,
	- install python swiftclient, 
	- install blender, 
	- install ssmtp, 
	- update ssmtp config files.

2. In nova_code.py, replace the 'imageId' with your new snapshotID and evtl. other constants to fit your account.

3. Provide your App Elevator app with environment variables
	OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME

4. In Cloud Object Storage, create a container 'permanent' and script 'blender_run.py' in it. This is the file with the rendering script:

~~~
	import bpy
	scene=bpy.context.scene
	scene.render.image_settings.file_format='BMP'
	bpy.context.scene.render.resolution_x = 800
	bpy.context.scene.render.resolution_y = 480
	bpy.context.scene.render.filepath = 'rendered.bmp'
	bpy.ops.render.render(use_viewport = True, write_still=True)
~~~

5. In Cloud Object Storage, create a container 'rendered' and make this container public.

~~~
	$ swift post rendered
	$ swift post -r '.r:*' rendered
~~~

6. Replace the URL of the Object Store endpoint to fit yours in files

	- userdata.sh
	- templates/download.jinja

7. Push the code to App Elevator.
