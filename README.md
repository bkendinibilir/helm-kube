# helm-kube

Kubernetes Cluster specific Helm configuration.

## setup

Clone custom [helm charts repo](https://github.com/bkendinibilir/helm-charts).

Fill in your kubernetes context name in [captain.cfg](captain.cfg) and set path to the helm charts repo.

Install python requirements:

```
pip install -r requirements.txt
```

Install helm and do init:
```
brew install kubernetes-helm
helm init
```

## secrets

Add your secrets in [secrets.json](secrets.json):

```
{
    "website": {                            # <-- namespace
        "wordpress": {                      # <-- name
            "postgresUser": "wordpress",
            "postgresPassword": "123456"
        }
    }
}
```

## usage

Apply your changes:

`./captain.py`