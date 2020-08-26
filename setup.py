from distutils.core import setup

setup(
    name='Simfloat',
    description='Simulate binary floating point representations and arithmetic to IEEE 754 standards of arbitrary fixed precision, or to infinite precision, and different rounding modes',
    author='Rob Clewley',
    version='0.2',
    packages=['simfloat',],
    license='BSD 2-Clause',
    long_description=open('README.md').read(),
)
