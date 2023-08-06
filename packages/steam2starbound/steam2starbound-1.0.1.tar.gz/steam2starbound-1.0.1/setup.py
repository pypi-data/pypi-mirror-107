from setuptools import setup

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='steam2starbound',
    version='1.0.1',
    description='Copies mods from steam workshop to the starbound directory.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://git.brokenmouse.studio/ever/steam2starbound',
    author='EV3R4',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: System Administrators',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        'Natural Language :: English',
    ],
    keywords=['starbound'],
    packages=['steam2starbound'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'steam2starbound=steam2starbound.__main__:main',
        ],
    },
)
