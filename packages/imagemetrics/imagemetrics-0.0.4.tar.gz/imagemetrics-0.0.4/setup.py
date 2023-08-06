from setuptools import setup, find_packages

VERSION = '0.0.4'
DESCRIPTION = 'Package to calculate image metrics for a binocular stereo camera image'
LONG_DESCRIPTION = 'This package compares the left and right halves of a stereo camera '\
                   'image using the luminance and sharpness metrics to assess obstruction '\
                   'to the lenses'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="imagemetrics",
        version=VERSION,
        author="roshan bal",
        url="https://github.com/roshanbal",
        author_email="<rbal408@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
