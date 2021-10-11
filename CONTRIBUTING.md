# Contributing

## Getting started

1. Follow instructions to
[install poetry](https://python-poetry.org/docs/#installation).
2. Follow instructions to
[install pre-commit](https://pre-commit.com/#install)

After cloning the repo:

1. `poetry install`: Install project and all dependencies
(see __Dependency management__ below)
2. `pre-commit install`: Install pre-commit hooks
(see __Linting and Testing__ below)

### Classification profiles

Classification profiles are stored in a separate repo
[classification-profiles](https://gitlab.com/flywheel-io/public/classification-profiles).

This repo is stored as a git submodule at path
`fw_gear_file_classifier/classification-profiles`.

Ater cloning this repo you will need to first init the submodule, and then
update to the current version:

* `git submodule init`
* `git submodule update --recursive`

## Dependency management

This gear uses [`poetry`](https://python-poetry.org/) to manage dependencies,
develop, build and publish.

### Dependencies

Dependencies are listed in the `pyproject.toml` file.

#### Managing dependencies

* Adding: Use `poetry add [--dev] <dep>`
* Removing: Use `poetry remove [--dev] <dep>`
* Updating: Use `poetry update <dep>` or `poetry update` to update all deps.
  * Can also not update development dependencies with `--no-dev`
  * Update dry run: `--dry-run`

#### Using a different version of python

Poetry manages virtual environments and can create a virtual environment with
different versions of python, however that version must be installed on the
machine.  

You can configure the python version by using
`poetry env use <path/to/executable>`

#### Helpful poetry config options

See full options
[Here](https://python-poetry.org/docs/configuration/#available-settings).

List current config: `poetry config --list`

* `poetry config virtualenvs.in-project <true|false|None>`: create virtual
environment inside project directory
* `poetry config virtualenvs.path <path>`: Path to virtual environment
directory.

## Linting and Testing

Local linting and testing scripts are managed through
[`pre-commit`](https://pre-commit.com/).  Pre-commit is configured to use
[qa-ci](https://gitlab.com/flywheel-io/tools/etc/qa-ci)

### pre-commit usage

* Run hooks manually:
  * Run on all files: `pre-commit run -a`
  * Run on certain files: `pre-commit run --files test/*`
* Update (e.g. clean and install) hooks:
`pre-commit clean && pre-commit install`
* Disable all hooks: `pre-commit uninstall`
* Enable all hooks: `pre-commit install`
* Skip a hook on commit: `SKIP=<hook-name> git commit`
* Skip all hooks on commit: `git commit --no-verify`

## Adding a contribution

Every contribution should be associated with a ticket on the GEAR JIRA board,
or be a hotfix.  You should contribute by creating a branch titled with
either `hotfix-<hotfix_name` or `GEAR-<gear_num>-<description>`.  For now,
other branch names will be accepted, but soon branch names will be rejected if
they don't follow this pattern.

When contributing, make a Merge Request against the main branch.

### Merge requests

The merge request should contain at least two things:

1. Your relevant change
2. Update the corresponding entry under `docs/release_notes.md`

Adding the release notes does two things:

1. It makes it easier for the reviewer to identify what relevant changes they
should expect and look for in the MR, and
2. It makes it easier to create a release.

#### Populating release notes

For example, if the gear is currently on version `0.2.1` and you are working on a
bugfix under the branch GEAR-999-my-bugfix.  When you create a merge request
against `main`, you should add a section to `docs/release_notes.md` such as the
following:

```markdown
## 0.2.2
BUG:
* Fixed my-bug, see [GEAR-999](https://flywheelio.atlassian.net/browse/GEAR-999)

```

Where the rest of the file contains release notes for previous versions.

### Creating a release

See
[Creating a release in qa-ci](https://gitlab.com/flywheel-io/tools/etc/qa-ci#creating-a-release)

## Updating classification-profiles

Since classification profiles are a submodule, updating is as easy as
changing into the directory and pulling the new changes, then adding
the directory and commiting:

1. `cd fw_gear_file_classifier/classification-profiles`
2. `git pull origin <branch>`
3. `cd ../../`
4. `git add fw_gear_file_classifier/classification-profiles`
5. `git commit -m "Updated classification-profiles"`
