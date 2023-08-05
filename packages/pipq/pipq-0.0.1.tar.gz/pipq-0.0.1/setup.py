
from setuptools import find_packages, setup

with open("requirements.txt") as f:
	requirements = f.readlines()

setup(
    name="pipq",
    version="0.0.1",
    packages=find_packages(),
    author="Error104114",
    description="Yet another pip search",
    license="GPL",
    install_requires=requirements,
    url = "",
    entry_points ={
            'console_scripts': [
                'pipq = pipq.pipq:main'
            ]
        },
    keywords ='pipsearch pip search find package python details',
    classifiers =(
    	"Development Status :: 2 - Pre-Alpha",
    	"Operating System :: OS Independent"            
        )   
)