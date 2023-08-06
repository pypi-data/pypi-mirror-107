from setuptools import setup, find_packages

VERSION = '0.0.9' 
DESCRIPTION = 'short Mail sender'
LONG_DESCRIPTION = 'Mail sender gmail smtp'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="andriatina_mail_sender", 
        version=VERSION,
        author="Andriatina Ranaivoson",
        author_email="andriatina@aims.ac.za",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        #scripts=['dokr'],
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'mail package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)