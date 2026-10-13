# Security Policy

## Scope

This policy covers the `hum2song` Python host, the extension loader, and
the in-tree extension modules under `src/hum2song/extensions/`.

## Threat model

The extension loader executes third-party code by design. Treat any
extension you install the same way you treat a browser plugin: it runs
with your user's privileges and can read your files.

- The host loads extensions from a configured search path only.
- Extensions must ship a signed `extension.toml` if loaded from a
  remote registry (see `config/registry.toml`).
- The native pitch extension uses `ctypes`; it does not shell out.

## Reporting a vulnerability

Email `security@hum2song.dev` with a repro. Do not open a public issue
for loader sandbox escapes or memory-safety bugs in `native_pitch`.

## Supported versions

Only the latest minor release receives security fixes.