# packaging tutorial

This is a tutorial on setting up python packages for PyPi. Steps were learned from:
https://www.youtube.com/watch?v=GIF3LaRqgXo&t=1281s


## Installation

## Executable function
 
def say_hello():
    print('Hello World')
    
name = input('What is your name?\n')
print ('Hi, %s.' % name)

# Notes

1)	From the folder level with setup.py : python setup.py sdist bdist_wheel
    a.	Builds a wheel that is appropriate to upload to PyPi
2)	pip install –e .
    a.	installs it locally. Tests packaging.
    b.	The ‘–e’ allows it to link to the code you are working on rather than building copies . The ‘ .’ means install in the current directory. Everytime you change the setup.py file you need to run this
3)	Test it:
    a.	python from packaging_tutorial import say_hello
        i.	‘packaging_tutorial’ is the py_module
        ii.	The name ‘hellototi’ is from setup.py -> name=’hellototi’. It is the name of the python script in the src folder. Within this script is the function say_hello
4)	Remove excessive files with gitignore.io
5)	Pip install twine
    a.	Twine upload dist/*
