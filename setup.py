from setuptools import setup, find_packages

setup(
    name='cmsplugin-journal',
    version='0.1.1',
    description='This is a news app/plugin for the django-cms 2.1',
    author='Fajran Iman Rusadi',
    author_email='fajran@gmail.com',
    url='http://bitbucket.org/fajran/journal/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)
