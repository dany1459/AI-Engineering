def get_sentences(path):

    f = open(path, 'r')                          # open file in read mode
    lines = f.readlines()                        # read each line in the file
    sentences = [line.split() for line in lines] # get a list of lists of all words in each line
                                                 # each line is a list
    return sentences

def clean(sentences):

    i = 0
    while i < len(sentences):

        if sentences[i] == []:      # check if the list is empty
            sentences.pop(i)        # remove empty lists
        else:                       # element on the right will move to the left on deletion
            i += 1                  # only increase the counter var if the list is not empty
    
    return sentences

def get_dictionaries(sentences):   # generate tokenizer

    vocab = []                     # tokenizer

    for sentence in sentences:     # iterate through all sentences
        for token in sentence:     # iterate through all words
            if token not in vocab: # add token to tokenizer if it is not there
                vocab.append(token)
    
    w2i = {w: i for (i, w) in enumerate(vocab)} # word to index
    i2w = {i: w for (i, w) in enumerate(vocab)} # index to word

    return w2i, i2w, len(vocab)



sent = get_sentences(".//13. Text Enc/blakepoems.txt")
sent = clean(sent)
w2i, i2w, l = get_dictionaries(sent)
print(w2i['You'], i2w[0], l)
