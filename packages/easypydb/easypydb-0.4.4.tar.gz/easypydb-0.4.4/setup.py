from distutils.core import setup
setup(
  name = 'easypydb',
  packages = ['easypydb'],
  version = '0.4.4',
  license='MIT',
  description = 'Simple and easy-to-use python database',
  author = 'Nayoar',
  author_email = 'nayoar8128@gmail.com',
  url = 'https://github.com/Nayoar/easypydb',
  download_url = 'https://github.com/Nayoar/easypydb/archive/v_02.tar.gz',
  keywords = ['database', 'db', 'easy', 'simple'],
  install_requires=[
          's1db',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)