from setuptools import setup, find_packages
 
setup( 
    name="ciscounityapi", 
    version="0.0.1", 
    description="Cisco Unity API for Python", 
    long_description=""" 
        Cisco Unity API for Python
    """, 
    author = "JFK",
    author_email = "info@jfk.rocks",
    url="https://github.com/",
    packages=['ciscounityapi'],
    install_requires=[ 
        'requests == 2.22.0',
    ],
    python_requires='>=3.5'
)