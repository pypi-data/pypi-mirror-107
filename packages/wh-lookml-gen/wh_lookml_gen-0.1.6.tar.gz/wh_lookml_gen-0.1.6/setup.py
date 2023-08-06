import pathlib
from setuptools import setup,find_packages

here = pathlib.Path(__file__).parent


setup (

    name='wh_lookml_gen',
    version='0.1.6',
    package_dir={'lookml_gen': 'src'},


    install_requires = [

        'pandas_gbq==0.15.0',
        'pandas_redshift==2.0.5',
        'pandas==0.24.2',
        'lkml==1.1.0',
        'GitPython==3.1.17',
        'protobuf==3.17.1',
        'PyYAML==5.4.1'

    ],
    entry_points={
        'console_scripts': [
            'lookml_gen_main=__main__:main',
            'lookml_gen_init = profile_generator:main',
            'lookml_gen=lookml_gen.__main__:main'

       ],

    },
)