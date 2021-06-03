# {{Skeleton Gear}}
This was created from [poetry-cow-says](https://gitlab.com/flywheel-io/flywheel-apps/templates/poetry-cow-says). 
Some things (packages in .toml, GUIDELINES.md, `tests/test_main.py` methods) 
were removed to remove conflicts for new gears. This gear does
not do anything, just used as a "bare bones" template.

This section provides an overview of what this gear implements. Please modify this file according to your gear information.  

#### __Note__: `DOCKER_HUB` var in `.gitlab-ci.yml` has changed to `false`. By default, this should be set to `true`

#### TODO: In `.env` file, we have changed the coverage to `0`; please modify that to 90% for critical gears and 70-90% for all others.

## Usage

### Inputs

* __{{text-file}}__: {{A text file containing text to say.}}

### Configuration
* __debug__ (boolean, default False): Include debug statements in output.


## Contributing

For more information about how to get started contributing to that gear, 
checkout [CONTRIBUTING.md](CONTRIBUTING.md).
