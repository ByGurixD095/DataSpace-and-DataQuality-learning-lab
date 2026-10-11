#!/usr/bin/env bash
# Compila los dos runtimes: connector.jar (consumidores) y provider.jar (proveedor, con proxy de data plane).
# Necesita Java 17+ y acceso a Maven Central (descarga las dependencias de EDC 0.18.1 la primera vez).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
./gradlew :runtime:connector:shadowJar :runtime:provider-proxy:shadowJar
ls -lh runtime/connector/build/libs/connector.jar runtime/provider-proxy/build/libs/provider.jar
