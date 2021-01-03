from setuptools import setup

setup(name='redlooper',
      version='0.1',
      description='Raspberry Pi Looper Pedal',
      author='Basil',
      author_email='basil.huber@gmail.com',
      packages=['redlooper', 'redlooper.gui'],
      install_requires=['cython', 'pyliblo', 'JACK-Client', 'RPi.GPIO'],
      entry_points={'console_scripts': ['redlooper=redlooper.main:main']},
      zip_safe=False)
