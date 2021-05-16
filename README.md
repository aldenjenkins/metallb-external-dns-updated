# Cloudflare Metallb External-DNS Dynamic A Record updating using WAN IP

Use TXT records created using external-dns to create corresponding A records

## Example helmfile.yaml

```
environments:
  default:
    values:
      - "../values.yaml.gotmpl"

repositories:
  - name: bitnami
    url: https://charts.bitnami.com/bitnami

releases:
  - name: external-dns-cloudflare
    chart: bitnami/external-dns
    namespace: external-dns-cloudflare
    values:
      - rbac:
          create: true
        sources: [ingress]
        policy: "create-only"
        provider: cloudflare
        cloudflare:
          apiKey: {{ .Values.tls.cloudflare.api_key }}
          email: {{ .Values.tls.cloudflare.email }}
          proxied: true
```
