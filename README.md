
# StylePhish

This is the official implementation of "StylePhish:A Set Transformer Based Approach for Phishing Detection via Brand Website Visual Styles"

The repository contains code and datasets required to reproduce the experiments and results presented in our paper.

## Table of Contents
1. [Overview](#overview)
2. [Setup](#setup)
3. [Input](#input)
4. [Contributing](#contributing)


## Overview
There are three main components in this projects:

1.  **PhishBaseline** - Contains the code and instructions required to reproduce the baseline methods reported in our paper (e.g., we use Serper API as a replacement for Google Search API in PhishLLM since Google Search API is no longer available for new users).

2.  **Dataset** - Contains the datasets used in our experiments and the scripts for data preprocessing.

3.  **Source Code** - Contains the implementation of our model, including training and evaluation scripts.

4.  **User Study** - Contains all user study-related materials.


## Setup
The virtual environment file is located as follows：
1. StylePhish Environment - `StylePhish/Source Code/stylephish_environment.yml`


### Environment & Activation
```bash
conda env create --name stylephish --file=stylephish_environment.yml
```


The environments can be activated using the following commands:

```
conda activate stylephish
```


## Input 

The input `--folder` must contain one sub-directory per site:


```
test_site_xxx/
├── info.txt    # the URL (required)
├── shot.png    # the screenshot (required)
└── html.txt    # the HTML source (optional)
```

## Contributing 
👪
For StylePhish, pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. For any detailed clarifications/issues, please email to songhuaibo@icloud.com.
