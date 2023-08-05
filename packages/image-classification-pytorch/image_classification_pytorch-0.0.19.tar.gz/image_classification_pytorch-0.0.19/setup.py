from distutils.core import setup
import os

# from os import path
# this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

# with open('README.md') as f:
#     readme = f.read()

here = os.path.abspath(os.path.dirname(__file__))

# What packages are required for this module to be executed?
try:
    with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
        REQUIRED = f.read().split('\n')
except:
    REQUIRED = []

setup(
    name='image_classification_pytorch',  # How you named your package folder (MyLib)
    packages=['image_classification_pytorch'],  # Chose the same as "name"
    version='0.0.19',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Image classification with pretrained models in Pytorch',  # Give a short description about your library
    long_description="See description on GitHub",
    long_description_content_type='text/markdown',
    author='Denis Potapov',  # Type in your name
    author_email='potapovdenisdmit@gmail.com',  # Type in your E-Mail
    url='https://github.com/denred0/image_classification_pytorch',
    # Provide either the link to your github or to your website
    download_url='https://github.com/denred0/image_classification_pytorch/archive/refs/tags/0.0.19.tar.gz',
    # I explain this later on
    keywords=['pytorch', 'image classification', 'imagenet', 'pretrained model'],
    # Keywords that define your package best
    install_requires=[
        'pytorch-lightning==1.2.10',
        'albumentations==0.5.1',
        'numpy==1.20.2',
        'opencv-python==4.5.1.48',
        'sklearn==0.0',
        'timm==0.4.5',
        'torch==1.8.1',
        'torchmetrics==0.2.0',
        'tqdm==4.60.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
