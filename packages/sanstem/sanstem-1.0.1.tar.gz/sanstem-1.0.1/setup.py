from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(

  name="sanstem",
  version="1.0.1",
  author="Sooraj S Nair",
  author_email="nairsooraj2000@gmail.com",
  description=("A rule-based stemmer for Sanskrit Verbs and Nouns"),
  license="MIT",
  keywords="Sanskrit Stemmer",
  url="https://github.com/sooraj-nair/sanstem",
  packages=['sanstem'],
  package_data={'sanstem': ['Data/*.csv']},
  long_description_content_type='text/markdown',
  long_description=README,
  
  install_requires=[            
          'devatrans',
          'polyglot',
  ],
  
  include_package_Data=True,
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
