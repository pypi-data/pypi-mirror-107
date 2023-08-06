from distutils.core import setup
setup(
  name = 'plogger-ls',
  packages = ['plogger'],
  version = 'v0.0.7',
  license='MIT',
  description = 'Uma biblioteca que junta logging e print',
  author = 'Leandro de Souza',
  author_email = 'leandrodesouzadev@gmail.com',
  url = 'https://github.com/leandrodesouzadev/plogger',
  download_url = 'https://github.com/leandrodesouzadev/plogger/archive/refs/tags/v0.0.7.tar.gz',
  keywords = ['logging', 'print'], 
  install_requires=[ ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)