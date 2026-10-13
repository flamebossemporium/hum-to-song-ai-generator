# Contributing to hum-to-song-ai-generator

Thanks for wanting to help humans turn humming into full tracks. This
project is a plugin host: a Python core that loads extension modules
written in Python, C++, C#, or Java. Read the plugin contract before
opening a PR.

## Repo layout

- `src/hum2song/host/` — the plugin host: loader, registry, lifecycle.
- `src/hum2song/pipeline/` — core stages: pitch, tempo, arrangement, render.
- `src/hum2song/extensions/` — in-tree extension modules (native_pitch,
  dotnet_vocodec, jvm_formant).
- `src/hum2song/contracts/` — shared protocol definitions every
  extension implements.
- `cmd/` — CLI entry points.
- `tests/` — pytest suite for the host and pipeline.

## Adding an extension

1. Create a package under `src/hum2song/extensions/<your_ext>/`.
2. Implement `hum2song.contracts.PitchExtension` (or `VocodeExtension`,
   `FormantExtension`).
3. Declare it in your package's `extension.toml` manifest.
4. The host auto-discovers manifests on startup — no central registry
   edit needed.
5. Add a test under `tests/extensions/` that loads your extension
   through the host loader.

## Style

- Python: `ruff` + `black`, line length 100.
- C++: C++20, `clang-format` with the repo `.clang-format`.
- C#: .NET 8, nullable enabled.
- Java: JDK 21, `google-java-format`.

## Pull requests

- One extension or one pipeline stage per PR.
- Include a short clip demonstrating before/after if it changes audio
  output.
- Update `docs/EXTENSIONS.md` if you add a new contract method.