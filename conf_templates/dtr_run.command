docker run -it --rm \
  --name {{docker_dtr_srv}} mirantis/dtr:2.8.2 install  \
  --dtr-external-url {{swarm_main_url}} \
  --ucp-node {{swarm_init}} \
  --ucp-username {{ucp_admin}} \
  --ucp-password {{ucp_pwd}} \
  --ucp-insecure-tls \
  --ucp-url https://{{hostlist[inventory_hostname]['ip']}}