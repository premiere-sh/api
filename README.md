# Premiere Protocol API

[![License](https://img.shields.io/github/license/piotrostr/premiere-api?color=blue)](https://github.com/piotrostr/premiere-api/blob/master/LICENSE)
![Test](https://github.com/piotrostr/premiere-api/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/premiere-sh/api/branch/master/graph/badge.svg?token=WZMNTI0JJN)](https://codecov.io/gh/premiere-sh/api)

## Usage

[Docs](https://api.premiere.sh/docs) (OpenAPI format)

## Requirements

- [git](https://docs.github.com/en/get-started/quickstart/set-up-git)
- [docker](https://docs.docker.com/) and [docker-compose]('https://docs.docker.com/compose/')

In order to run without containers, running postgresql database service locally
and using python executable also works

- [python](https://www.python.org/downloads/)
- [postgresql](https://www.postgresql.org/download/)

## Development

### Containerized

Create `.env` file with contents:

```sh
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=pw
POSTGRES_HOST=db
```

In order to run tests:

```sh
docker-compose run api pytest --cov=. --cov-report=html
```

### Locally

With the postgresql server running on port 5432:

```sh
pip install -r requirements.txt
pytest --cov=. --cov-report=html
```

Linting is done through [pyright](https://github.com/microsoft/pyright) and for
formatting use [yapf](https://github.com/google/yapf).

## Additional Remarks

Games are going to be fixed and added based on the business needs,
warzone is going to be the first implementation. At first there will only be
one platform, probably cross-play stemming from battle.net

If it would end up being crypto-based, there could be a L2 Arbitrum smart
contract to keep track of everything safely on chain.

Below are some loose thoughts from previous meetings with the stakeholders.

```solidity
contract Premiere {

    // this would probably require merkle proofs for checking the players

    struct Tournament {
        uint entryPrice;
        uint currentPlayerId;
        uint startDate;
        uint playerCap;
        uint winnerAddress;
    }

    mapping(uint => Tournament) public tournaments;

    function joinTournament(uint tournamentId) {
        Tournament tournament = tournaments[tournamentId];
        require(tournament.currentPlayerId < tournament.playerCap);
        // ...
    }

    function finalise(Tournament t, address winner) external onlyAuthorized {
        // withdraw(winnerAddress);
        // withdraw to the winner, write the tournament as done
    }

    function getBestPlayer() external view {
        // storage is quite expensive, but a function that loops through
        // and only reads could be very cheap computation-wise
    }
}
```

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
SECRET_KEY=***
```

where the `SECRET_KEY` is an `openssl rand -hex 32` hash.

```bash
kubectl create secret generic premiere-secrets --from-env-file=./.env
```

```sh
kubectl apply -f manifest.yml
```
