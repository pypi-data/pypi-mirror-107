from setuptools import setup

setup(name='cue',
      version='0.5',
      description='Accounting system for linux',
      author='Jonas McCallum',
      author_email='jonasmccallum@gmail.com',
      url='https://kosciuszko.cloud',
      packages=['cue',
                'cue.cli',
                'tests'],
      package_data={'': ['*.yml',
                         '*.txt',
                         '*.jnl',
                         '*.acc']},
      install_requires=['ruamel.yaml'],
      extras_require={'testing': ['pytest']},
      entry_points={'console_scripts': ['cue = cue.cli.bin:cue']},
      zip_safe=False)
