from setuptools import setup

setup(
    name='Simfloat',
    description='Simulate binary floating point representations and arithmetic to IEEE 754 standards of arbitrary fixed precision, or to infinite precision, and different rounding modes',
    author='Rob Clewley',
    version='0.2',
    packages=['simfloat',],
    license='BSD 2-Clause',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
            "Topic :: Education",
            "Topic :: Scientific/Engineering"
        ],
    url="https://github.com/robclewley/ieee754_simulation",
    install_requires=['numpy']
)
