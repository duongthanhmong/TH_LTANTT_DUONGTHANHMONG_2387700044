"""Restore stdlib TLS for this application after startup truststore injection."""
import importlib
import ssl


def restore_stdlib_ssl():
    module = ssl.SSLContext.__module__
    if module in ("pip._vendor.truststore._api", "truststore._api"):
        truststore = importlib.import_module(module.rsplit(".", 1)[0])
        truststore.extract_from_ssl()
    if ssl.SSLContext.__module__ != "ssl":
        raise RuntimeError("SecureChat requires the standard library ssl.SSLContext")


restore_stdlib_ssl()
