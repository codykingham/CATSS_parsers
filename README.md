# CATSS

The CATSS database ("Computer Assisted Tools for Septuagint Studies") is a Septuagint
database with morphology and Hebrew text alignments (BHS) with text-critical notes. The 
database can be publicly accessed at [http://ccat.sas.upenn.edu/rak//catss.html](http://ccat.sas.upenn.edu/rak//catss.html),
and can be retrieved as plain text files. The user must agree to the CATSS' unfortunately
limited license. It is not good that this license is so closed, and in the future it 
would be great to see it opened up as Creative Commons. 

## Purpose of these tools

While the CATSS database is published online, the dataset is provided in a complicated format
which makes using that data difficult. This repository contains a number of Python methods
which can be used to automatically retrieve the data and convert it into easy-to-use json
files. This is especially crucial with the alignment ("parallel") files, which are quite 
complicated in their arrangement.

Another goal of this repo is to update, where relevant, the documentation for the alignment
dataset, since some notations have not been updated in the docs.

## Promoting Open-use of CATSS

Though the CATSS dataset is not provided under a permissive license, it is still published
freely online. It is hoped that the development of these tools will encourage more people 
to use the CATSS dataset, which in turn will hopefully encourage the license holders to release
it under a more open license.

## Source Data

Note that due to the license, the CATSS data itself is not stored in this repository. But you can
run `get_source_data.py` to download the files to your copy of the repo.
