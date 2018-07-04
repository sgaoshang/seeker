import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='seeker',
    version='1.0.0',
    url='https://github.com/sgaoshang/seeker',
    license='BSD',
    maintainer='sgao',
    maintainer_email='sgao@redhat.com',
    description='customer portal case seeker',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
