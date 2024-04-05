# python-template

This is a template for Python-based repositories.

## Usage

The recommended way to use this repo is to

1. **Use this project as template**: and then run copier locally. Simply click on the "Use this template" button on the GitHub page to create a new repository based on this template.

2. **Run copier**: you can download [Copier](https://github.com/copier-org/copier) and then run the following command:

```bash
copier copy "https://github.com/armand-sauzay/python-template.git" <your_folder>
```

If you want to target a specific branch, you can use:

```bash
copier copy --vcs-ref "<python-template-branch>" "https://github.com/armand-sauzay/python-template.git" <target-folder>
```

## Project files

### .commitlintrc.json and .releaserc.json

These files are used by `semantic-release` to determine the type of the next release. The `.commitlintrc.json` file is used to lint the commit messages. The `.releaserc.json` file is used to determine the version of the next release based on the commit messages. To lint commit messages, this project uses the default configuration of `@commitlint/config-conventional`.

### .python-version file

The `.python-version` file contains the python version used in this project. This project has been built with using `pyenv` as python version manager.

### .pre-commit-config.yaml

This file is used by `pre-commit` to determine the hooks that will be run before each commit. The hooks are defined in the `hooks` section of the file. The hooks are run in the order they are defined in the file.

### .github/workflows

This repository uses Github Actions for CI/CD. CI is composed of `Lint` with pre-commit and `Test` with pytest. Release is composed of `Lint`, `Test`, `Release` with semantic-release.

- Lint is done with [pre-commit](https://pre-commit.com/). To run lint locally, run `pre-commit run --all-files`.
- Test is done with [pytest](https://docs.pytest.org/en/8.0.x/). To run test locally, run `pytest`. Or poetry run `pytest` if you use poetry as package manager.
- Release is done with [semantic-release](https://github.com/semantic-release/semantic-release)
