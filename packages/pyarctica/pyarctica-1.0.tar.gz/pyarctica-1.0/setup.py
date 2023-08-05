from distutils.core import setup
setup(
  name = 'pyarctica',
  packages = ['pyarctica'],
  version = '1.0',
  license='MIT',
  description = 'Python wrapper and alerts trigger',
  author = 'Ilan Z., Elad S.',
  author_email = 'ilan@arctica.ai',
  url = 'https://github.com/user/pysnowly',
  download_url = 'https://github.com/snowly-io/pyarctica/archive/v_01.tar.gz',
  keywords = ['Arctica Trigger'],
  install_requires=[
          'snowflake-connector-python',
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)