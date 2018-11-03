from setuptools import setup

setup(
        name='aws_vpn_config',
        version='0.1.0',
        description= 'Download VPN Configurations and convert to vendor config (As same as Download Configuration from AWS console).\n Examples:  $ python vpn-config.py download --vpn-id vpn-08cad142f9189e87d -c 10. $ python vpn-config.py list',
        author='Anderson dos Santos',
        author_email='adsantos@gmail.com',
        url='https://github.com/asantos2000/aws_vpn_config/',
        packages=['aws_vpn_config'],
        scripts=['scripts/aws-vpn-config'],
        install_requires=[
                'sh',
                'boto3',
                'lxml',
                'xmltodict',
                'prettytable'
        ],
        license='BSD',
        platforms='Unix',
        classifiers=[
                'Operating System :: Unix',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.7',
        ],
)
