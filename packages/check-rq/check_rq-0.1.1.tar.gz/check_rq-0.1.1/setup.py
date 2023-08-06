import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='check_rq',
    version='0.1.1',
    author='Crafter B.V.',
    author_email='koen@getcrafter.com',
    url='https://github.com/crafterwerkbon/check_rq',
    description='Icinga/Nagios check for RQ (Redis Queue)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=[
        'nagiosplugin',
        'rq',
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'check_rq=check_rq.check_rq:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
