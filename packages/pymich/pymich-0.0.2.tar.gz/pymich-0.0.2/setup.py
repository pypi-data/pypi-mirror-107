from setuptools import setup


setup(
    name='pymich',
    version='0.0.2',
    setup_requires='setupmeta',
    install_requires=['pytezos'],
    extras_require=dict(
        test=[
            'freezegun',
            'pytest',
            'pytest-cov',
        ],
    ),
    author='Thomas Binetruy',
    author_email='tbinetruy@gmail.com',
    url='https://yourlabs.io/piratzlabs/pymich',
    include_package_data=True,
    license='MIT',
    keywords='cli',
    python_requires='>=3.9',
)
