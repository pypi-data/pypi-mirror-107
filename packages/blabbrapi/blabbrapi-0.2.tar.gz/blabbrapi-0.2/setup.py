from distutils.core import setup
setup(
  name = 'blabbrapi',
  packages = ['blabbrapi'],
  version = '0.2',
  license='MIT',
  description = 'The official Python API to communicate with the Blabbr website',
  author = 'Team Blabbr: --VSCoder-- (A1pha), Xenity',
  author_email = 'scratch.xenity@gmail.com',
  url = 'https://blabbr.xyz',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['Python', 'Blabbr', 'API', 'Bot'],
  install_requires=[
          'urlopen',
          'json',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)