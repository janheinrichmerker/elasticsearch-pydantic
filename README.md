<!-- markdownlint-disable MD041 -->
[![PyPi](https://img.shields.io/pypi/v/elasticsearch-pydantic?style=flat-square)](https://pypi.org/project/elasticsearch-pydantic/)
[![CI](https://img.shields.io/github/actions/workflow/status/janheinrichmerker/elasticsearch-pydantic/ci.yml?branch=main&style=flat-square)](https://github.com/janheinrichmerker/elasticsearch-pydantic/actions/workflows/ci.yml)
[![Code coverage](https://img.shields.io/codecov/c/github/janheinrichmerker/elasticsearch-pydantic?style=flat-square)](https://codecov.io/github/janheinrichmerker/elasticsearch-pydantic/)
[![Python](https://img.shields.io/pypi/pyversions/elasticsearch-pydantic?style=flat-square)](https://pypi.org/project/elasticsearch-pydantic/)
[![Issues](https://img.shields.io/github/issues/janheinrichmerker/elasticsearch-pydantic?style=flat-square)](https://github.com/janheinrichmerker/elasticsearch-pydantic/issues)
[![Commit activity](https://img.shields.io/github/commit-activity/m/janheinrichmerker/elasticsearch-pydantic?style=flat-square)](https://github.com/janheinrichmerker/elasticsearch-pydantic/commits)
[![Downloads](https://img.shields.io/pypi/dm/elasticsearch-pydantic?style=flat-square)](https://pypi.org/project/elasticsearch-pydantic/)
[![License](https://img.shields.io/github/license/janheinrichmerker/elasticsearch-pydantic?style=flat-square)](LICENSE)

# 🔍 elasticsearch-pydantic

Use the [Elasticsearch DSL](https://github.com/elastic/elasticsearch-dsl-py) with [Pydantic](https://github.com/pydantic/pydantic) models.

This minimal library is for those who...

- ... want to benefit from Pydantic's [extensive validation and type checking](https://docs.pydantic.dev/latest/concepts/models/) ecosystem,
- ... want the convenient and idiomatic [persistence layer](https://elasticsearch-dsl.readthedocs.io/en/latest/tutorials.html#persistence) and [query DSL](https://elasticsearch-dsl.readthedocs.io/en/latest/tutorials.html#search) of Elasticsearch DSL,
- ... and do not want to reimplement everything from scratch.

To interconnect the Elasticsearch DSL and Pydantic, we override a limited set of methods from the Elasticsearch [`Document`](https://elasticsearch-dsl.readthedocs.io/en/latest/api.html#elasticsearch_dsl.Document) and `InnerDoc` base classes with Pydantic's [`BaseModel`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel) functionality. Elasticsearch field types are inferred from the model's type annotations and can be overridden by using [`Annotated`](https://docs.python.org/3/library/typing.html#typing.Annotated) type hints.

## Installation

Install the package from PyPI:

```shell
pip install elasticsearch-pydantic
```

## Usage

> TODO

### Examples

More examples can be found in the [`examples`](examples/) directory.

### Compatibility

This library works fine with any of the following Pip packages installed:

- `elasticsearch8`
- `elasticsearch-dsl`
- `elasticsearch6-dsl`
- `elasticsearch7-dsl`
- `elasticsearch8-dsl`

The `elasticsearch-pydantic` library will automatically detect which Elasticsearch DSL is installed.

## Development

To build this package and contribute to its development you need to install the `build`, `setuptools` and `wheel` packages:

```shell
pip install build setuptools wheel
```

(On most systems, these packages are already pre-installed.)

### Development installation

Install package and test dependencies:

```shell
pip install -e .[tests]
```

### Testing

Verify your changes against the test suite to verify.

```shell
ruff check .  # Code format and LINT
mypy .        # Static typing
pytest .      # Unit tests
```

Please also add tests for your newly developed code.

### Build wheels

Wheels for this package can be built with:

```shell
python -m build
```

## Support

If you have any problems using this package, please file an [issue](https://github.com/janheinrichmerker/elasticsearch-pydantic/issues/new).
We're happy to help!

## License

This repository is released under the [MIT license](LICENSE).
