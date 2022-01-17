# k8s-tcpdump-webhook

A simple tcpdump sidecar injector to demonstrate Kubernetes's Mutating Webhook

## Build and Deploy

Build docker image;

`docker build -t bilalunalnet/tcpdump-webhook .`

Generate private key and certificate for SSL connection.

```
openssl req -new -sha256 \
     -newkey rsa:2048 \
     -subj "/C=TR/ST=Istanbul/O=tcpdump-webhook/CN=tcpdump-webhook.webhook-demo.svc" \
     -nodes -x509 \
     -days 365 \
     -out server.crt \
     -addext "subjectAltName = DNS:tcpdump-webhook.webhook-demo.svc"
```

Update ConfigMap data in the `manifest/webhook-deployment.yaml` file with your key and certificate.

Update `caBundle` value in the `manifest/webhook-configuration.yaml` file with your base64 encoded certificate.

`cat server.crt | base64 -w0`

```
kubectl create ns webhook-demo
kubectl apply -f manifest/webhook-deployment.yaml
kubectl apply -f manifest/webhook-configuration.yaml
```
## Test

There is a Pod manifest file in the `manifest` directory to be used for testing purposes. The Pod has `tcpdump-sidecar` label to meet the condition in the `app/mutator.py` file.