import numpy as np



def get_glove_embeddings_from_sentences(texts, download_model=False):
    '''
    A function to extract glove embeddings(300 dimensions) from a text corpus.

    Parameters:
        texts : A list of strings

        Returns: a list of arrays
    '''
    #Confirming the sentences are in string format
    texts = [str(text) for text in texts]
    
    #First download and unzip the glove pretrained file into directory.
    if download_model != False:
        try:
            # !wget http://nlp.stanford.edu/data/glove.6B.zip
            # !unzip glove*.zip
            print("skipped model")

        except:
            print("downloading the model files failed. Please manually download and extract the file from: http://nlp.stanford.edu/data/glove.6B.zip")

    # load the whole embedding into memory
    embeddings_index = dict()
    f = open('glove.6B.300d.txt')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    print('Loaded %s word vectors.' % len(embeddings_index))


    sentence_vectors = []
    for text in texts:
        if len(text) != 0:
            text_vector = sum([embeddings_index.get(w, np.zeros((300,))) for w in text.split()])/(len(text.split())+0.001)
        else:
            text_vector = np.zeros((300,))
        sentence_vectors.append(text_vector)
    print("Extraction completed.")
    return sentence_vectors