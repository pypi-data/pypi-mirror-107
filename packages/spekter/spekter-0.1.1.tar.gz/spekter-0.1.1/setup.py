from setuptools import setup, find_packages

setup(
    name='spekter',
    version='0.1.1',
    packages=find_packages(), 
    include_package_data=True, 
    install_requires=[
        'Click',
        'Flask==1.1.2',
        'sonic_client==0.0.5',
        'dulwich==0.20.21',
        'Fabric==2.6.0',
        'python-dotenv==0.17.1'
    ],
    entry_points={
        'console_scripts': [
            'spekter = spekter.main:cli',
        ],
    },
)