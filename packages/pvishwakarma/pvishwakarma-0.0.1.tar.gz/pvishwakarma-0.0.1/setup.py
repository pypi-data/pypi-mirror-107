from setuptools import setup, find_packages

classifiers = [
'Development Status :: 5 - Production/Stable',
'Intended Audience :: Education',
'Operating System :: Microsoft :: Windows :: Windows 10',
'License :: OSI Approved :: MIT License',
'Programming Language :: Python :: 3'

]

setup(
    name='pvishwakarma',
    version='0.0.1',
    description='Python Library',
    Long_Description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='PV',
    author_email='pvishwakarma@adaequare.com',
    License='MIT',
    classifiers=classifiers,
    keywords='library',
    packages=find_packages(),
    install_requires=['']
)