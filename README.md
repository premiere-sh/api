# Premiere Backend

docker-compose env file contains:

```sh
POSTGRES_USERNAME= ***
POSTGRES_PASSWORD= ***
POSTGRES_HOST= ***
```

there needs to be a kubernetes secret created for k8s deployments:

```bash
kubectl create secret generic premiere-secrets --from-env-file=./.env
```
