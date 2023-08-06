from distutils.core import setup

setup(
    name='daspuml-compiler',
    packages=['daspuml-compiler'],
    version='0.1',
    license='MIT',
    description='TYPE YOUR DESCRIPTION HERE',
    author='YOUR NAME',
    author_email='your.email@domain.com',  # Type in your E-Mail
    # url='https://github.com/user/reponame',  # Provide either the link to your github or to your website
    # download_url='https://github.com/user/reponame/archive/v_01.tar.gz',  # I explain this later on
    keywords=['SOME', 'MEANINGFULL', 'KEYWORDS'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'validators',
    ],
)
