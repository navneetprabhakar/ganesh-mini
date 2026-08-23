FROM node:22-bookworm-slim@sha256:a17d50af28002a160548bd4225b3cfcb12c5efcb171f79e68758f2885fb1b066
LABEL org.ganesh.verifier.base-manifest="sha256:a17d50af28002a160548bd4225b3cfcb12c5efcb171f79e68758f2885fb1b066" \
      org.ganesh.verifier.typescript-version="5.5.4" \
      org.ganesh.verifier.typescript-integrity="sha512-Mtq29sKDAEYP7aljRgtPOpTvOfbwRWlS6dPRzwjdE+C0R4brX/GUyhHSecbHMFLNBLcJIPt9nl9yG5TZ1weH+Q=="
COPY --chmod=0444 assets/typescript-5.5.4.tgz /opt/typescript-5.5.4.tgz
COPY --chmod=0555 typescript-probe.sh /usr/local/bin/typescript-probe
WORKDIR /work
