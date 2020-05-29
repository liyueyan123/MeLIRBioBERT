<p align="center">
<img src="https://github.com/it21208/MeLIR/blob/master/MeLIR-logo.png" width="360">
</p>

This repo contains PyTorch and BioBERT DL model for document classification.

MeLIR BioBERT is designed for Python 3.6 and PyTorch 0.4. PyTorch recommends Anaconda for managing your environment. We'd recommend creating a custom environment as follows:

conda create --name melir python=3.6


Python packages we use can be installed via pip:

pip install -r requirements.txt


Code depends on data from NLTK (e.g., stopwords) so you'll have to download them:

import nltk
nltk.download()
