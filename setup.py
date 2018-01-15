from distutils.core import setup
from setuptools import find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(name='eve-s3storage',
      version='0.1',
      description='python-eve S3 MediaStorage extension',
      author='Gabriel Wainer',
      author_email='gabrielcw@gmail.com',
      packages=find_packages(),
      install_requires=reqs,
      include_package_data=True,
      zip_safe=False,
      url='https://github.com/gwainer/eve-s3storage',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      )
