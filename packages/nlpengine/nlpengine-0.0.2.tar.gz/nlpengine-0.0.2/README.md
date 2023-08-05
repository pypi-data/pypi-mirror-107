# NLP Engine

**nlpengine** is a collection of Natural Language Processing functions. Its designed to make a NLP engineer's life easier by bundling some of the everyday tasks like data cleaning, feature extraction, text classification, etc. This module is built on top of other popular open source python libraries.

# Installation

```python
pip install nlpengine
```

# Features

 The key featues in the initial release of **nlpengine** includes:
 

 - [ ] Easy to use text classifiers
 - [ ] Vectorization of texts
 - [ ] Active Learning (in development)
 - [ ] Several utility functions

### Text Classifier

 A wrapper on top of Facebook's **[FastText](https://github.com/facebookresearch/fastText)** text classifier to build a text classifier with just few lines of codes.
	 
   ```python
texts = ["sample sentence one", "just another sentence!", "is this a sentence?"]
labels = ["not question", "not question", "question"]

from nlpengine.classifiers import FastTextClassifier
clf = FastTextClassifier()
model = clf.fit(text, labels)
```

   

### Convert texts to vectors

This module helps convert a corpus of texts to a vector matrix easily. This extracted matrix could be used for further downstream tasks such as text similiarity, vector decomposition & visualization, etc.

```python
from nlpengine.feature_extraction import def get_glove_embeddings_from_sentences
texts = ["a great sentence", "and a meaningful one"]
vectors = get_glove_embeddings_from_sentences(texts, download_model=True)