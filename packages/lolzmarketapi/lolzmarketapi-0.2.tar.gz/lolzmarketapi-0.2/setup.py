from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(name='lolzmarketapi',
      version='0.2',
      description='Использование функций маркета через python',
      packages=['marketapi'],
      long_description=long_description,
      long_description_content_type='text/markdown', 
      author_email='cotanton111@gmail.com',
      zip_safe=False)
