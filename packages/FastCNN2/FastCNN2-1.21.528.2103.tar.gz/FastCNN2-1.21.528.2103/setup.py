from setuptools import setup


"""
set App Name
"""
name = "FastCNN2"
version = '1.21.0528.2103'

author = "Iuty"
author_email = "dfdfggg@126.com"

"""
set entry_points
"""
entry_points={
        'console_scripts': [
            "gongda = FastCNN.entry.gongda:main"
        ]
    }

"""
set dependents
"""

install_requires = [
        #"IutyLib"
        ]

"""
set pip install packages 
"""
packages = [
        "FastCNN.entry",
        "FastCNN.prx",
        
        ]

setup(
    name=name,
    version= version,
    author = author,
    author_email = author_email,
    packages=packages,
    entry_points=entry_points,
    install_requires = install_requires
)