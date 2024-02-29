# Generate Self-Signed Certificate for RabbitMQ

To use a self-signed certificate for RabbitMQ, follow these steps:

1. Generate a private key:
```bash
openssl genrsa -out rabbitmq.key 2048
```

2. Create a certificate signing request (CSR):
```bash
openssl req -new -key rabbitmq.key -out rabbitmq.csr -subj "/CN=localhost"
```

3. Generate a self-signed certificate using the private key and the CSR:
```bash
openssl x509 -req -days 365 -in rabbitmq.csr -signkey rabbitmq.key -out rabbitmq.crt
```

After running these commands, you will have the following files:

- `rabbitmq.key`: The private key.
- `rabbitmq.csr`: The certificate signing request.
- `rabbitmq.crt`: The self-signed certificate for RabbitMQ.

You can then configure your RabbitMQ server to use `rabbitmq.key` and `rabbitmq.crt` for enabling secure connections.
