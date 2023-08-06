from setuptools import setup
data="""
 Welcome.This Module has 2 main functions: ReadCSV and WriteCSV. To know more, type:
        ```
        `
        python -m pip install csvreader
        ```
        or 
        
        ```
        python3 -m pip install csvreader
        ```
        
        Windows: 
        
        ```
        py -m pip install csvreader
        ```
"""
setup(
    name = 'csvreader',
    version = '0.0.4',
    description = 'A Library that Reads and Writes CSV Files Quickly.',
    long_description = data,
    author = 'SF Publishing',
    install_requires = ['pip','setuptools','wheel','virtualenv'],
    packages = ['csvreader']
)
