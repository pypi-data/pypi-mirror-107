from setuptools import setup,find_packages


setup(
   name='BeeDB',
   version='1.6',
   description='BeeDB it is an easier way to make a simple database',
   license="MIT",
   long_description=open('README.txt').read(),
   author='Zaid Ali',
   author_email='realarty69@gmail.com',
   keywords=['db','database','json'],
    packages=['beedb'],
    package_dir={'beedb': 'beedb'},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)