from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='track-it',
  version='0.0.1',
  description='Hand Tracking Machine Learning Module',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sunami Dasgupta',
  author_email='sunamidasgupta@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='handtracking', 
  packages=find_packages(),
  install_requires=['opencv-python','mediapipe'] 
)