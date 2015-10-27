from setuptools import setup

#with open('requirements.txt', 'r') as fh:
#    dependencies = [l.strip() for l in fh]

setup(
    name='cImage',
    description='Relational algebra on top of pandas DataFrames ',
    version='1.0.0',
    py_modules = ['reframe'],
    author = 'Brad Miller',
    author_email = 'bonelake@mac.com',
    install_requires= ['pandas>=0.16.0'],
    include_package_data = False,
    license='GPL',
    url = 'https://github.com/bnmnetp/relation',
    keywords = ['database', 'relational'], # arbitrary keywords
    classifiers=('Development Status :: 5 - Production/Stable',
                   'Environment :: Console',
                   'Intended Audience :: Education',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Operating System :: MacOS',
                   'Operating System :: Unix',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Education'),
    long_description=open('README.rst').read(),
)
