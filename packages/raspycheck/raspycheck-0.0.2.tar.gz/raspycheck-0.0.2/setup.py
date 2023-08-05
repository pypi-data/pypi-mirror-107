from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='raspycheck',
    version='0.0.2',
    description='Useful tool to execute commands via SSH on a RPI or grab system info from said RPI',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Felix Harenbrock',
    author_email='felix.harenbrock@gmx.de',
    keywords=['Raspberry Pi', 'Raspi', 'RPI'],
    url='https://github.com/kampfhamster309/raspycheck',
    test_suite='nose.collector',
    tests_require=['nose']
    #download_url='https://pypi.org/project/elastictools/'
)

install_requires = [
    'paramiko==2.7.2',
    'termcolor==1.1.0'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
