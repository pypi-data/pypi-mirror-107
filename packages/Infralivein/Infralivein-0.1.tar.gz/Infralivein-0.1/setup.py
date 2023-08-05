from distutils.core import setup
setup(
  name = 'Infralivein',         # How you named your package folder (MyLib)
  packages = ['Infralivein'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Vein detection helper Function',   # Give a short description about your library
  author = 'Mirza Riyasat Ali',                   # Type in your name
  author_email = 'mirzariyasatali1@domain.com',      # Type in your E-Mail
  url = 'https://github.com/MirzaRiyasatAli/Infrali74.git',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/MirzaRiyasatAli/Infrali74.git',    # I explain this later on
  keywords = ['Veindetecting', 'Python', 'Veinfinder', 'Veinlocator', 'Veindetection'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'opencv-python',
          'numpy',
          'matplotlib',
          'os',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',

  ],
)