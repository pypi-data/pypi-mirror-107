import setuptools
with open("README.md", "r") as fh:
  long_description = fh.read()
setuptools.setup(  
    name = 'mediaiobest1213123123',  
    version = '0.0.6',
    author = 'wucm',  
    author_email = 'wucm@gmail.com',	
    description = 'get a chinesename by random',
    long_description=long_description,
    long_description_content_type="text/markdown",    
	url = "http://www.xxx.com",
    packages=setuptools.find_packages()
)  
