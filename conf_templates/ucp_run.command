docker container run --rm -it -v /var/run/docker.sock:/var/run/docker.sock \
  --name {{docker_ucp_srv_name}} docker/ucp:3.3.0 install  \
  --host-address {{hostlist[inventory_hostname]['ip']}} \
  --admin-password {{ucp_pwd}} \
  --admin-username {{ucp_admin}} \
  --force-minimums