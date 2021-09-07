# BookReport
Our Data Mining project, a prediction model based on data from bookdipository.com.

## Run Project
#### Creating the DB
either:
1. Run /BookDepository/bookdepository_crawler_slices.py
2. Move all the slices to /dbSlices
3. Run /dbSlices/mergeFilesScript.py

or:
1. Run /BookDepository/bookdepository_crawler.py
2. Move the output file to /dbSlices

#### Preprocess data
1. Run xl_preprocess.py
2. Run df_preprocess.py

#### Run model and evaluation
1. run model.py

## Creators
- Netzer Epstein [https://github.com/netzer-git]
- Tal Eliram
