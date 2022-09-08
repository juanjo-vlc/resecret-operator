# DISCLAIMER: WIP Do not use in production
This is a #learnbydoing project, not suitable for production use

# Motivation
Working with automated deployments and helm charts or operators, is not easy, as they are often maintained by different teams, and built for different purposes.

In my case, I tried the [Crunchy postgres operator](https://operatorhub.io/operator/postgresql) and the [Keycloak legacy operator](https://operatorhub.io/operator/keycloak-operator) and both work well, but the secret containing connection data created by the postgres operator is not what keycloak is expecting.

# Description
This operator tackles the issue by defining a new custom resource, called ReSecret which defines where to find the information and how it should be called. For ease of use, the reference follows the same structure as the when referencing secrets on Pods or PodTemplates, so kubernetes users are already familiar with it.

The name ReSecret was chosen because the prefix "Re" means repetition, but it can also be understood as reference.

# Usage
In order to use this operator the following steps should be performed:
1.- Download the code
```sh
git clone https://github.com/juanjo-vlc/resecret-operator.git \
  && cd resecret-operator
```

2.- Get the default values and tailor them to fit your needs
```sh
helm show values resecret-operator/ |tee my-values.yml
```

3.- Deploy the helm chart
```sh
helm upgrade --install -n MY_NAMESPACE MY_RELEASE_NAME resecret-operator \
  --create-namespace -f my-values.yml
```

4.- Create an object of kind ReSecret and deploy it into your cluster:
```sh
cat <<EOF | my-resecret.yaml
apiVersion: juanjo.garciaamaya.com/v1alpha1
kind: ReSecret
metadata:
  name: keycloak-pg-db
  labels:
    app: keycloak
spec:
  name: keycloak-db-secret-resecret
  secrets:
    - key: POSTGRES_DATABASE
      secretKeyRef:
        name: keycloak2-postgrescluster-pguser-keycloak
        key: dbname
    - key: POSTGRES_EXTERNAL_ADDRESS
      value: a2V5Y2xvYWsyLXBvc3RncmVzY2x1c3Rlci1oYS5hbHRrZXljbG9hay5zdmMuY2x1c3Rlci5sb2NhbA==
    - key: POSTGRES_EXTERNAL_PORT
      value: NTQzMg==
    - key: POSTGRES_PASSWORD
      secretKeyRef:
        name: keycloak2-postgrescluster-pguser-keycloak
        key: password
    - key: POSTGRES_USERNAME
      secretKeyRef:
        name: keycloak2-postgrescluster-pguser-keycloak
        key: user
    - key: SSLMODE
      value: cmVxdWlyZQ==
EOF

kubectl -n my-namespace -f my-resecret.yml
```

# Specifying literal values on resecret
If literal values have to be included on the created secret they could be specified directly on the ReSecret object as base64-encoded data in the ```value``` property instead of using a ```secretKeyRef``` object.
