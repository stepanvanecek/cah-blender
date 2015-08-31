from novaclient.v2 import client as nvclient


def start_vm(container_up_name, obj_name, container_downloads, environ, mail):
    nv = nvclient.Client(username=environ['OS_USERNAME'],
                         project_id=environ['OS_TENANT_NAME'],
                         api_key=environ['OS_PASSWORD'],
                         auth_url=environ['OS_AUTH_URL'],
                         insecure=False)

    flavor = nv.flavors.find(name="cloudcompute.xs")
    secgroup = nv.security_groups.find(name="default")
    image_id = "a812a1ab-bf8c-46a9-9fa4-439a585d09a5"

    # keypair and ssh rule needed only for debug purposes
    key_name = 'firstKeypair'

    have_ssh_rule = False
    for rule in secgroup.rules:
        if rule['ip_protocol'] == "tcp" and rule['from_port'] == 22 and rule['to_port'] == 22:
            have_ssh_rule = True
            break
    if not have_ssh_rule:
        nv.security_group_rules.create(secgroup.id,
                                       ip_protocol="tcp",
                                       from_port=22,
                                       to_port=22)

    userdata_script = get_userdata(container_up_name, obj_name, container_downloads, environ, mail)

    nv.servers.create(name=obj_name,
                      image=image_id,
                      flavor=flavor.id,
                      key_name=key_name,    # debug purposes
                      availability_zone='nova',
                      security_groups=['default'],
                      userdata=userdata_script)


# replace the strings in userdata script template to get customised script
def get_userdata(container_up_name, obj_name, container_down_name, environ, mail):
    with open('userdata.sh') as udata:
        script = udata.read()\
            .replace('userdata_container_uploads', container_up_name)\
            .replace('userdata_filename', obj_name)\
            .replace('userdata_container_downloads', container_down_name)\
            .replace('userdata_url', environ['OS_AUTH_URL'])\
            .replace('userdata_tenant_name', environ['OS_TENANT_NAME'])\
            .replace('userdata_user', environ['OS_USERNAME'])\
            .replace('userdata_pass', environ['OS_PASSWORD'])\
            .replace('userdata_email', mail)
    return script
