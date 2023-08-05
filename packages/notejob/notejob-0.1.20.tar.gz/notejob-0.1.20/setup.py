from os import path

from notebuild.tool import read_version
from setuptools import find_packages, setup

version_path = path.join(path.abspath(path.dirname(__file__)), 'script/__version__.md')


install_requires = ['apscheduler', 'gunicorn', 'flask-migrate', 'flask-script']

setup(name='notejob',
      version=read_version(version_path),
      description='notejob',
      author='niuliangtao',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',
      entry_points={'console_scripts': ['notejob = notejob.core:notejob']},
      packages=find_packages(),
      package_data={"notejob": ["*", "*.html", "*.js", "*.*"]},
      #include_package_data=True,
      install_requires=install_requires
      
      )
