from setuptools import setup

setup(name='cue',
      version='0.3',
      description='Accounting system for linux',
      author='Jonas McCallum',
      author_email='jonasmccallum@gmail.com',
      url='https://kosciuszko.cloud',
      packages=['cue',
                'cue.cli'],
      package_data={'cue.cli': ['templates/settings.yml',
                                'templates/invoice.txt',
                                'templates/token_spec.yml']},
      install_requires=['ruamel.yaml'],
      extras_require={'testing': ['pytest']},
      entry_points={'console_scripts': ['cue = cue.cli.bin:cue']},
      zip_safe=False)
