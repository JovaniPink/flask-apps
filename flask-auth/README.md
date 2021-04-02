# Flask

A starter authentication webhook for Hasura GraphQL Engine written in Python
using Flask... for GraphQL!

## Configure Hasura

Configure Hasura with the webhook url. You will need to set an admin secret key to
enable webhook.

When running Hasura as a docker container, `localhost` will point to the
container itself, not the host machine. So, if you're running the webhook
locally or as a container (not on a public url), you'll need to:

1. Use [`docker network`](https://docs.docker.com/engine/reference/commandline/network/) and
   keep Hasura and the webhook container in the same network so that webhook url
   will become `http://container-id:5000/auth-webhook`
2. Linux: Bind both containers on host network (use `--net=host` with docker
   run) so that `localhost` will be the host's network itself. Here, webhook url
   will be `http://localhost:5000/auth-webhook`
3. Mac: If webhook is running on the host, url will be
   `http://host.docker.internal:5000/auth-webhook`

Set the following environment variables for Hasura:

```
HASURA_GRAPHQL_ADMIN_SECRET=myadminsecretkey
HASURA_GRAPHQL_AUTH_WEBHOOK=http://localhost:5000/auth-webhook
```

All queries will be now validated through the webhook.

> Read more on [authentication and access control](https://hasura.io/docs/1.0/graphql/manual/auth/index.html).
