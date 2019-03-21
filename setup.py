from setuptools import setup


def fetch_version():
      '''
      Fetches version variable from version.py
      '''
      version = {}

      with open('midihelper/version.py') as f:
            exec(f.read(), version)

      return version['__version__']



setup(name='midihelper',
      version=fetch_version(),
      description='MIDI Helper',
      url='http://github.com/UCLeuvenLimburg/midihelper',
      author='Frederic Vogels',
      author_email='frederic.vogels@ucll.be',
      license='MIT',
      install_requires=['mido'],
      packages=['midihelper'],
      entry_points = {
            'console_scripts': [ 'midihelper=midihelper.command_line:shell_entry_point']
      },
      zip_safe=False)