import numpy as np

def preprocess(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace('.', '').replace(',', '').replace(':', '').replace(';', '').replace('!', '').replace('?', '').replace('-', '').replace('_', '').replace("\"", '').replace("\'", '').replace('[', '').replace(']', '')

        with open('12. Embeddings/preprocessed.txt', 'w') as p:
            p.writelines(lines)


def get_sentences(path):
    f = open(path, 'r')
    lines = f.readlines()
    sentences = [line.lower().split() for line in lines]
    f.close()

    return sentences


def clean_sentences(sentences):
    i = 0
    while i < len(sentences):
        if sentences[i] == []:
            sentences.pop(i)
        else:
            i += 1
    
    return sentences


def get_dictionaries(clean_sentences):
    vocabulary = []
    for sentence in clean_sentences:
        for token in sentence:
            if token not in vocabulary:
                vocabulary.append(token)

    word2index = {word: index for (index,word) in enumerate(vocabulary)}
    index2word = {index: word for (index,word) in enumerate(vocabulary)}

    return word2index, index2word, len(vocabulary)


def get_pairs(sentences, word2index, r):
    pairs = []
    for sentence in sentences:
        tokens = [word2index[word] for word in sentence]
        for center in range(len(tokens)):
            for context in range(-r, r+1):
                context_word = center + context
                if context_word < 0 or context_word >= len(tokens) or context_word == center:
                    continue
                else:
                    pairs.append( (tokens[center], tokens[context_word]) )

    return np.array(pairs)


def get_dataset():
    sentences = get_sentences('12. Embeddings/preprocessed.txt')
    clean_sent = clean_sentences(sentences)
    word2index, index2word, len_vocabulary = get_dictionaries(clean_sent)
    pairs = get_pairs(clean_sent, word2index, 4)

    return pairs, len_vocabulary


# preprocess('12. Embeddings/blakepoems.txt')

# sentences = get_sentences('12. Embeddings/preprocessed.txt')
# clean_sent = clean_sentences(sentences)
# print(len(sentences), len(clean_sent))

# word2index, index2word, len_vocabulary = get_dictionaries(clean_sent)

# print(word2index['poems'])
# print(index2word[0])
# print(len_vocabulary)

# pairs, _ = get_dataset()
# print(pairs[0])
