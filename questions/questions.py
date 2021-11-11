import math
import nltk
import sys

import os
import string
from collections import Counter

import pdb

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as file:
            name = file.name.split('/')[1]
            content = file.read().replace('\n', '')

            files[name] = content

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document.lower())

    stopwords = nltk.corpus.stopwords.words("english")
    punctuation = string.punctuation

    words = [word for word in words if word not in stopwords]
    words = [word for word in words if word not in punctuation]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs_values = dict()

    single_words = [word for document in list(documents.values()) for word in document]
    single_words = list(dict.fromkeys(single_words))

    for word in single_words:
        documents_containing_word = 0

        for file, words in documents.items():
            if word in words:
                documents_containing_word += 1

        idfs_values[word] = math.log(len(documents) / documents_containing_word)

    return idfs_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    files_scores = dict()

    for word in query:
        word_frequency = 0

        for file, words in files.items():
            if word in words:
                word_frequency += Counter(files[file])[word]

            files_scores[file] = word_frequency * idfs[word]

    top_files_list = sorted(files_scores, key=files_scores.get, reverse=True)[:n]

    return top_files_list


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
