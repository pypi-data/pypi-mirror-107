from setuptools import find_packages, setup

setup(
    name='lologging',
    packages=find_packages(),
    version='0.3.0',
    description='This is a library meant to provide meaningful logging for python cloud run services on GCP',
    author_email = 'clement.voisin@loreal.com',
    author='Clément Voisin',
    license='MIT',
    url = 'https://github.com/loreal-IT-France/itfr-btdp-pyPI-lib-lologging',
    download_url = 'https://github.com/loreal-IT-France/itfr-btdp-pyPI-lib-lologging/archive/refs/tags/0.3.0.tar.gz',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)

