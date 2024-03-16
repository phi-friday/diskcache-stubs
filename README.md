# diskcache-stubs

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-yellow.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/diskcache-stubs.svg)](https://badge.fury.io/py/diskcache-stubs)
[![python version](https://img.shields.io/pypi/pyversions/diskcache-stubs.svg)](#)

Warning: This library provides type hints only.
If you need the runtime package,
you can find it [`python-diskcache`](https://github.com/grantjenks/python-diskcache).

## how to install
```shell
$ pip install diskcache-stubs
```

## TODO
* [ ] `diskcache.core.Cache`
> `Cache.pull`, `Cache.peek`, `Cache.peekitem`
* [ ] `.typeshed.BaseCache`
> `BaseCache.get`, `BaseCache.pop`
* [ ] `diskcache.djangocache.DjangoCache`
> Lack of interest in `Django`, so I haven't modified most of it since it was auto-generated.
* [ ] tests?

## License

Apache 2.0, see [LICENSE](https://github.com/phi-friday/diskcache-stubs/blob/main/LICENSE).
