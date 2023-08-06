from setuptools import setup
import pypandoc


def get_version(path):
    with open(path, "r") as fp:
        lines = fp.read()
    for line in lines.split("\n"):
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(name='torch-trafo',
      version=get_version("torch_trafo/__init__.py"),
      description='PyTorch implementation of transformer block layers.',
      # long_description=pypandoc.convert('README.md', 'rst'),
      # url='http://github.com/ulf1/torch-trafo',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='Apache License 2.0',
      packages=['torch_trafo'],
      install_requires=[
          'torch>=1.1.0,<2'
      ],
      python_requires='>=3.6',
      zip_safe=True)
