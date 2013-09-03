import os
from setuptools import setup, find_packages

readme = open(os.path.join(os.path.dirname(__file__), 'README'))
README = readme.read()
readme.close()

version = __import__('odesk').get_version()


setup(name='python-odesk',
      version=version,
      description='Python bindings to oDesk API',
      long_description=README,
      author='oDesk',
      author_email='python@odesk.com',
      maintainer='Kirill Panshin',
      maintainer_email='kamelok@odesk.com',
      install_requires=['oauth2', 'urllib3'],
      packages=find_packages(),
      license = 'BSD',
      download_url ='http://github.com/odesk/python-odesk',
      url='http://odesk.github.com/python-odesk',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities',],)
