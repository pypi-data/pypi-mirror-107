from distutils.core import setup
setup(
  name = 'CryptICE',         # How you named your package folder (MyLib)
  packages = ['CryptICE'],   # Chose the same as "name"
  version = '1.0.2-r1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'ICE cipher for Python',   # Give a short description about your library
  author = 'Ren',                   # Type in your name
  author_email = 'zeze839@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Sam839/CryptICE',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Sam839/CryptICE/releases/tag/1.0.2',    # I explain this later on
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
  ],
)