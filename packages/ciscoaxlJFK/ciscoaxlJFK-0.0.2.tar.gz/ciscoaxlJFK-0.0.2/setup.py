from setuptools import setup, find_packages
 
setup( 
    name="ciscoaxlJFK", 
    version="0.0.2", 
    description="custom AXL/SQL Package", 
    long_description=""" 
        custom AXL/SQL Package by JFK
    """, 
    author = "JFK",
    author_email = "info@jfk.rocks",
    url="https://github.com/",
    packages=['ciscoaxlJFK'],
    install_requires=[ 
        'zeep == 3.4.0', 
        'urllib3 == 1.23', 
        'requests == 2.22.0',
        'six == 1.12.0',
    ],
    python_requires='>=3.8'
)