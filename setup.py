from distutils.core import setup

setup(
    name='market-maker-keeper',
    version='1.0.0',
    packages=[
        'market_maker_keeper',
        'models'
    ],
    url='https://github.com/captain13128/auction-keeper',
    license='',
    author='',
    author_email='',
    description='',
    install_requires=[
        "pymaker==1.2.*",
        "pygasprice-client==1.0.*",
        "forex_python",
        "ccxt",
    ]
)
