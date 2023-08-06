#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='lb_dsnd_distributions',
      version='0.0.3',
      packages=['lb_dsnd_distributions'],
      author= 'Lisa Banh',
      author_email= 'contact.lisabanh@gmail.com',
      description='Gaussian & Binomial distributions',
      long_description = long_description,
      long_description_content_type = "text/markdown",
      classifiers =[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
      ],
      zip_safe=False)

