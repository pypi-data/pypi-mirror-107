from setuptools import setup

# `python3 setup.py bdist_wheel` :
#       to generate build.
# `python3 setup.py sdist` :
#       to generate source distributable.
# `pip3 install -e .` :
#       to install the package in development
#       it also helps ensure installation works correctly

with open('README.md') as f:
    long_description = f.read()

classifiers = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
]

# install_requires should be flexible for all compatible versions.
install_requires=[
    'blessings ~= 1.7',
    ]

# extra_require should be very specific to provide identical dev environment
extras_require = {
    "dev": [
        "pytest>=3.7",
        'check-manifest', # This is needed to create manifest file that includes all files in sdist as in out git repo.
        ]
}

setup(
    # Mandatory settings
    name='mmhelloworld',
    version='0.0.1',
    url='https://github.com/manasm11/mmhelloworld.git',
    author='Manas Mishra',
    author_email='manas.m22@gmail.com',
    description='Say Hello!',
    py_modules=['mmhelloworld'],
    package_dir={'':'src'},

    # Optionals
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    extras_require=extras_require,
)
