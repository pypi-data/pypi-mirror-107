from distutils.core import setup

setup(
    name='daspuml-compiler',
    packages=['daspuml-compiler'],
    version='0.2',
    license='MIT',
    description='TYPE YOUR DESCRIPTION HERE',
    author='YOUR NAME',
    author_email='your.email@domain.com',  # Type in your E-Mail
    # url='https://github.com/user/reponame',  # Provide either the link to your github or to your website
    keywords=['UML'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'validators',
    ],
    entry_points={
        'console_scripts': [
            'daspuml-compiler = daspuml-compiler.main:main'
        ]
    },
)
