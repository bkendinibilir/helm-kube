# helm-kube

Kubernetes Cluster specific Helm configuration.

## secrets.json

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
