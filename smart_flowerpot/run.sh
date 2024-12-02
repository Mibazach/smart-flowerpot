#!/bin/bash

export DJANGO_SECRET_KEY="-kgxn9%xxgz=t=5y7-264g-0#l6ndhu+ztf1f3qz$ubzsawqbo"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="*,localhost,127.0.0.1"
export DB_ENGINE="django.db.backends.sqlite3"

GUNICORN_WORKERS=3
GUNICORN_BIND="0.0.0.0:443"
GUNICORN_TIMEOUT=120

CERT_DIR="/var/www"
CERT_FILE="$CERT_DIR/server.crt"
KEY_FILE="$CERT_DIR/server.key"

mkdir -p "$CERT_DIR"

if [ ! -f "$CERT_FILE" ] || [ ! -f "$KEY_FILE" ]; then
    echo "SSL certificate or key not found. Generating new SSL certificates..."

    # Create OpenSSL config file for SAN
    OPENSSL_CONFIG="$CERT_DIR/openssl.cnf"
    cat > "$OPENSSL_CONFIG" <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = State
L = City
O = Organization
OU = Department
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
EOF

    # Generate SSL certificate and key
    openssl req -x509 -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" -days 365 -nodes -config "$OPENSSL_CONFIG"
    chmod 600 "$CERT_FILE" "$KEY_FILE"
    echo "SSL certificates generated: $CERT_FILE and $KEY_FILE"
fi

echo "Starting Gunicorn on https://$GUNICORN_BIND/"
gunicorn smart_flowerpot.wsgi:application \
    --workers $GUNICORN_WORKERS \
    --bind $GUNICORN_BIND \
    --timeout $GUNICORN_TIMEOUT \
    --log-level=info \
    --access-logfile - \
    --error-logfile - \
    --certfile="$CERT_FILE" \
    --keyfile="$KEY_FILE"
