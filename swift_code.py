import swiftclient
import datetime
import random


def check_file_exists(object_name, container_download, environ):
    try:
        swift = swiftclient.Connection(
            auth_version='2',
            user=environ['OS_USERNAME'],
            tenant_name=environ['OS_TENANT_NAME'],
            key=environ['OS_PASSWORD'],
            authurl=environ['OS_AUTH_URL'],
            )
    except swiftclient.exceptions.ClientException as e:
        print e

    try:
        swift.get_object(container_download, object_name)
        return True
    except swiftclient.exceptions.ClientException as e:
        return False


def upload_to_container(f, container_upload, environ):
    try:
        swift = swiftclient.Connection(
            auth_version='2',
            user=environ['OS_USERNAME'],
            tenant_name=environ['OS_TENANT_NAME'],
            key=environ['OS_PASSWORD'],
            authurl=environ['OS_AUTH_URL'],
            )
    except swiftclient.exceptions.ClientException as e:
        print e

    # check if the container exists
    try:
        swift.get_container(container_upload)
    except swiftclient.exceptions.ClientException as e:
        swift.put_container(container_upload)

    # create unique name for the object and upload it
    while True:
        try:
            object_name = 'obj' + str(datetime.datetime.now())\
                .replace(" ", "").replace(":", "")\
                .replace(".", "").replace("-", "")\
                + "r" + str(random.randint(1, 1000000000))
            swift.get_object(container_upload, object_name, f)
        except swiftclient.exceptions.ClientException as e:
            swift.put_object(container_upload, object_name, f)
            break
    return object_name
