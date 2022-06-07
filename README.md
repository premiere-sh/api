# ♦️ Premiere Protocol API.

## Project is not actively maintained! The setup below works and site is up in beta.

## Usage

[Docs](https://api.premiere.sh/docs) (OpenAPI format)

## Stack

FastAPI with PostgreSQL database, with user authentication and endpoints for
CRUD operations on tournaments and games. Running on Terraform-provisioned
Linode Kubernetes Engine cluster with NGINX node balancing with TLS.

## Deployment

### Networking

After provisioning with terraform (requires the `terraform.tfvars` file) and
getting the `kubeconfig.yml`, let's expose the cluster with an ingress:

```sh
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```

Then get the ipv4 of the ingress and point the domain (in this case
`api.premiere.sh`) to it. Note that the hostname has to be included in the
`manifest.yml`. Next, get cert:

```sh
kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.8.0/cert-manager.yaml
```

This should leave to `api.premiere.sh` being accessible both via `HTTP/HTTPS`
and returning 503 status from nginx.

### Services

Having exposed the cluster, deploy the resorces.

`.env` file contents:

```sh
POSTGRES_USERNAME=***
POSTGRES_PASSWORD=***
POSTGRES_HOST=***
```

```bash
kubectl create secret generic premiere-secrets --from-env-file=./.env
```

```sh
kubectl apply -f manifest.yaml
```
