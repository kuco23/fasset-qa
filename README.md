# FAssets QA

This is the QA repository for the FAssets project. It should empose a standard on a QA process for the project.

## Process

The FAssets QA repo follows the rules:

1. Tested code is included in the project's submodule,
2. The code configuration files are inside `fasset-bots-config`.


>**Warn**:
>Dockerfile relies on the state of the submodule. Remember to switch to the relevant branch before building.

## TODO:

- [ ] in _env.py map property method name to .env parameter name via decorator
- [x] in _config.py load variables from config.toml via dacite