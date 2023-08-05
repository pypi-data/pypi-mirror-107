import re
import sys
from os.path import join, dirname

from setuptools import setup, find_packages

with open(join(dirname(__file__), 'README.rst'), 'r', encoding='utf-8') as fd:
    long_description = fd.read()


def read_version():
    p = join(dirname(__file__), 'kikyo_bundle', '__init__.py')
    with open(p, 'r', encoding='utf-8') as f:
        return re.search(r"__version__ = '([^']+)'", f.read()).group(1)


version = read_version()

_ver = version.split('.')
kikyo_min_version = f'{_ver[0]}.{int(_ver[1])}'
kikyo_max_version = f'{_ver[0]}.{int(_ver[1]) + 1}'

install_requires = [
    f'kikyo>={kikyo_min_version},<{kikyo_max_version}',
    'PyYAML>=5.4.1',
    'packaging',
    'requests>=2.25.1',
    'pydantic>=1.7.3',
    'apache-bookkeeper-client>=4.12.1',
    'pulsar-client>=2.7.0,<2.8',
    'minio>=7.0.1,<8.0',
    'elasticsearch>=7.11.0,<8.0',
    'oss2>=2.14.0',
]


def main():
    if sys.version_info < (3, 6):
        raise RuntimeError('The minimal supported Python version is 3.6')

    setup(
        name='kikyo-bundle',
        version=version,
        description='kikyo bundle package',
        long_description=long_description,
        zip_safe=False,
        packages=find_packages(exclude=('tests',)),
        include_package_data=True,
        python_requires='>=3.6',
        install_requires=install_requires,
        entry_points={'kikyo.plugins': 'kikyo_bundle = kikyo_bundle.plugin'}
    )


if __name__ == '__main__':
    main()
