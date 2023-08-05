from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(name='youapi',
      version='0.1',
      description='Использование функций форума через python',
      packages=['pyyouapi'],
      long_description=long_description,
      long_description_content_type='text/markdown', 
      author_email='cotanton111@gmail.com',
      zip_safe=False)
