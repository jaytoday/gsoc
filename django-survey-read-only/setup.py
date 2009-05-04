from setuptools import setup, find_packages

setup(
    name='django-survey',
    version='0.0.2',
    description='A simple extensible survey application for django sites',
    author='Yann Malet, Doug Napoleone',
    author_email='yann.malet@gmail.com',
    url='http://code.google.com/p/django-survey/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)
