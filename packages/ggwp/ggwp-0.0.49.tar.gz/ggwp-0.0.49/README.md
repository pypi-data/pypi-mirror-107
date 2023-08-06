# ggwp: Prepare Fast, Analyze Faster  
[![PyPI Latest Release](https://img.shields.io/pypi/v/ggwp)](https://pypi.org/project/ggwp/) 
[![Downloads](https://img.shields.io/pypi/dm/ggwp)](https://pypi.org/project/ggwp/)
[![Repo Size](https://img.shields.io/github/repo-size/datanooblol/ggwp)](https://pypi.org/project/ggwp/)
[![License](https://img.shields.io/pypi/l/ggwp)](https://pypi.org/project/ggwp/)
[![Release Date](https://img.shields.io/github/release-date/datanooblol/ggwp)](https://pypi.org/project/ggwp/)

## What is ggwp?

**ggwp** is a Python package for fast and easy data analytics.  
It aims to make a data model that can be applied for some use cases  
such as customer analytics. The data model created by ggwp is designed  
directly from my personal experiences, which will be more and more data models  
in the future. In addition, **ggwp** now has some new features for  
logging, modeling and evaluating your models, which of these can speed up your workflow  
FOR REAL!!

## Main Features  
Here are current features available in **ggwp**  

```
from ggwp.EzDataModel import *
```
Example codes -> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1BcbHZjwNHsxtypOhu9KgddPOY28N5Xtt?usp=sharing)  
-  DataModel: prepare your raw data for a general data model
-  RFMT: create RFMT dataset
-  Cohort: create Cohort dataset
-  CustomerMovement: create Customer Movement dataset
-  BasketEvolving: create Basket Evolving dataset  

```
from ggwp.EzModeling import *
```
Example codes -> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uMNnpK-4x8wAq5pVsahWePnKzQNZdClK?usp=sharing)  
-  Check: check your data quality and more
-  Log: log your data, its status and your remark, so you know what you've done for each stage
-  Evaluation: evaluate your model using traditional (R2, RMSE, F-1, ACC, ROC) and practical metrics (Cost&Benefit, Lift)
-  BenchMark: benchmark your models' performances giving you some intuition  

```
from ggwp.EzPipeline import *
```
Example codes -> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1s4Rkpa53XxWn9GAfKFL9kot7Q44OMRum?usp=sharing)  

-  GroupImputer: impute your value with multiple subsets (as you desire)
-  ConvertVariables: convert all of your columns in one command  
-  ColumnAssignment: adding a new column in your pipeline is now available  
-  OneHotTransformer: the brand-new One-Hot-Encoding is now at your service
-  DataFrameTransformer: write your own function and use it along with your pipeline seamlessly


## Where to get **ggwp**  
The source code is currently hosted at GitHub:  
https://github.com/datanooblol/ggwp  

The latest version is available at  
[Python Package Index (PyPI)](https://pypi.org/project/ggwp/)  

```sh  
# pip  
pip install ggwp  
```  

## Dependencies  

-  numpy  
-  pandas  
-  sklearn
-  xgboost

## Disclaimer  
**ggwp** is now in devoping phase. Hence, if you experience any inconveniences, please be patient...