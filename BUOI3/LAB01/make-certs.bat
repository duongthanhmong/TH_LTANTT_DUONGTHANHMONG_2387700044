@echo off
setlocal enabledelayedexpansion

:: Di chuyen vao thu muc hien tai
cd /d "%~dp0"

:: Tao cac thu muc con
if not exist certs\ca mkdir certs\ca
if not exist certs\server mkdir certs\server
if not exist certs\client mkdir certs\client

echo ==============================
echo Tao Root CA
echo ==============================

openssl genrsa -out certs\ca\ca.key 2048

openssl req -x509 -new -nodes ^
-key certs\ca\ca.key ^
-sha256 ^
-days 3650 ^
-out certs\ca\ca.crt ^
-config openssl.cnf ^
-extensions v3_ca


echo.
echo ==============================
echo Tao Server Certificate
echo ==============================

openssl genrsa -out certs\server\server.key 2048

openssl req -new ^
-key certs\server\server.key ^
-out certs\server\server.csr ^
-subj "/C=VN/ST=HN/L=HN/O=MyOrg/OU=IT Dept/CN=localhost"

openssl x509 -req ^
-in certs\server\server.csr ^
-CA certs\ca\ca.crt ^
-CAkey certs\ca\ca.key ^
-CAcreateserial ^
-out certs\server\server.crt ^
-days 365 ^
-sha256 ^
-extfile openssl.cnf ^
-extensions v3_server


echo.
echo ==============================
echo Tao Client Certificate
echo ==============================

openssl genrsa -out certs\client\client.key 2048

openssl req -new ^
-key certs\client\client.key ^
-out certs\client\client.csr ^
-subj "/C=VN/ST=HN/L=HN/O=MyOrg/OU=IT Dept/CN=client"

openssl x509 -req ^
-in certs\client\client.csr ^
-CA certs\ca\ca.crt ^
-CAkey certs\ca\ca.key ^
-CAcreateserial ^
-out certs\client\client.crt ^
-days 365 ^
-sha256 ^
-extfile openssl.cnf ^
-extensions v3_client


echo.
echo ==============================
echo Kiem tra certificate
echo ==============================

openssl verify ^
-CAfile certs\ca\ca.crt ^
-purpose sslserver ^
certs\server\server.crt

openssl verify ^
-CAfile certs\ca\ca.crt ^
-purpose sslclient ^
certs\client\client.crt


echo.
echo ==============================
echo Cac chung chi da tao xong!
echo - CA:     certs\ca\
echo - Server: certs\server\
echo - Client: certs\client\
echo ==============================

pause