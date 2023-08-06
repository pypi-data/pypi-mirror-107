import setuptools

setuptools.setup(
    name='userElainaTestSetup1',
    version='1.8.2',
    description='Some small tols like syntactic sugar.',
    py_modules=['aaa'],
	# packages=['userElainaTestSetup1'],   
	packages=setuptools.find_packages(),

    long_description='',
    author='userElaina',
    author_email='userElaina@google.com',
    url='https://github.com/userElaina',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    keywords='qwq saya elaina test',
    install_requires=[
		'Pillow',
	],
    package_data={
        'userElainaTestSetup1': ['1.txt'],
    },
    python_requires='>=3.6',
)