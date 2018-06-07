import os
from setuptools import setup, find_packages

version = os.environ.get("VERSION")

setup(
    name='mixmorph',
    version=version,
    description='Mixmorph statechart processor',
    url='https://bitbucket.org/smart-space/smartbc',
    author='Stanislav Kraev',
    author_email='skraev@smart.space',
    license='Proprietary',
    # entry_points={
    #     'console_scripts': ['smart-space-svc=smartspace.scripts.smart_space_svc:main'],
    # },
    packages=find_packages(
        include=[
            'mixmorph',
            'mixmorph.*'
        ]
    ),
    #package_data={'smartspace': ['tests/test_config.cfg']},
    zip_safe=False,
    install_requires=[
        'pytest'
    ],
    python_requires='>=3.6,!=2.*',
    classifiers=[
        'Development Status :: 5 - Production',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3.6',
    ],
)
