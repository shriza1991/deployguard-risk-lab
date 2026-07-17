# Security Baseline

The main branch is expected to remain clean and secure:

- no committed secrets
- no public S3 buckets
- no root containers
- no privileged Kubernetes workloads
- no unrestricted security group ingress
- no deployment workflow that bypasses tests

Future risk scenarios should be introduced through branches and pull requests.

