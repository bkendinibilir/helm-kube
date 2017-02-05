# helm-kube

Kubernetes Cluster specific Helm configuration.

## setup

Clone custom [helm charts repo](https://github.com/bkendinibilir/helm-charts).

Fill in your kubernetes context name in [captain.cfg](captain.cfg) and set path to the helm charts repo.

## secrets

Add your secrets in [secrets.json](secrets.json):

```
{
    "website": {                             # <-- namespace
        "wordpress_postgresql": {            # <-- name_chart
            "postgresUser": "wordpress",
            "postgresPassword": "123456"
        }
    }
}
```

## usage

Apply your changes:

`./captain.py`