FROM node:22-bookworm-slim@sha256:a17d50af28002a160548bd4225b3cfcb12c5efcb171f79e68758f2885fb1b066
LABEL org.ganesh.verifier.base-manifest="sha256:a17d50af28002a160548bd4225b3cfcb12c5efcb171f79e68758f2885fb1b066" \
      org.ganesh.verifier.typescript-version="5.5.4" \
      org.ganesh.verifier.typescript-integrity="sha512-Mtq29sKDAEYP7aljRgtPOpTvOfbwRWlS6dPRzwjdE+C0R4brX/GUyhHSecbHMFLNBLcJIPt9nl9yG5TZ1weH+Q=="
RUN npm pack typescript@5.5.4 --ignore-scripts --registry=https://registry.npmjs.org/ \
    && echo "32dab6f6c28300460feda963460b4f3a94ef39f6f0456952e9d3d1cf08dd13e0b44786eb5ff194ca11d279c6c73052cd04b70920fb7d9e5f721b94d9d70787f9  typescript-5.5.4.tgz" | sha512sum --check --strict \
    && npm install -g ./typescript-5.5.4.tgz --ignore-scripts --no-audit --no-fund \
    && rm typescript-5.5.4.tgz
WORKDIR /work
