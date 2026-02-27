# Bootstrap

Bootstrap is a tiny CLI that prepares a target repo for automation.
- AI Agent setup
- Web app
- CI Setup with docker image build
- etc.

Anything defined in bootstrap-template.

## Install system-wide

```bash
pipx install .
```

Or with pip (editable, for development):

```bash
pip install -e .
```

After installation, the `bootstrap` command is available globally:

```bash
bootstrap <repo|path>
```

## Usage

```bash
bootstrap <repo|path>          # clone a repo and bootstrap it
bootstrap /path/to/existing    # use an existing local checkout
bootstrap <repo> --dest <dir>  # clone into a specific directory
```

## Behavior

- Clones the [bootstrap-template](https://github.com/reb00t-io/bootstrap-template) repo into a temp directory.
- Copies all template contents into the target repo.
- Runs `scripts/init.sh` from the target repo if present and a terminal is available.
