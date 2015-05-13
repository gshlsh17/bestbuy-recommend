import numpy
import argparse
import pickle
import directory
import load

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC


def construct_tf_idf_matrix(data, store=False):
    print "... TF-IDF Matrix Construct ..."

    # construct tf-idf normalized matrix for training data
    vectorizer = TfidfVectorizer(stop_words='english', charset_error='ignore')
    training_data = vectorizer.fit_transform(data)

    print "... TF-IDF Matrix Compelte ..."

    if store:
        print "... Dumping TFIDF Vectorizer ..."
        pickle.dump(vectorizer, open(directory.TFIDF_FILE, 'wb'))
        print "... Dumping Compelete ..."

    return training_data


def map_sku_to_label(sku, store=False):
    my_dict = dict()
    reverse_dict = dict()

    for i, value in enumerate(set(sku)):
        my_dict[value] = i
        reverse_dict[i] = value

    mapping_labels = numpy.zeros(shape=len(sku), dtype=numpy.int)
    for i, value in enumerate(sku):
        mapping_labels[i] = my_dict[value]

    if store:
        print "... Dumping Label SKU Mapping ..."
        pickle.dump(reverse_dict, open(directory.LABEL_SKU_MAPPING_FILE, 'wb'))
        print "... Dumping Complete ..."

    return mapping_labels


def train(training_data, training_labels, store=False):
    print "...Training Start ..."
    
    classifier = SVC(kernel='rbf', probability=True, C=2)

    classifier.fit(training_data, training_labels)

    print "... Training Complete ..."

    if store:
        print "... Classifier Dumping ..."
        pickle.dump(classifier, open(directory.CLASSIFIER__FILE, 'wb'))
        print "... Dumping Complete ..."

    # do this after pickling as it takes a while; we can run predict.py
    # while the score is computing.
    print "... Scoring start ..."
    print "Training Set Classification Accuracy: %s" % \
    classifier.score(training_data, training_labels)
    print "... Scoring Complete ..."


def run(store=False, run_diagnostics=False):
    data, skus = load.loadTrainingData()
    print "... Load Total Data Points: %d ..." % len(data)

    training_labels = map_sku_to_label(skus, store)
    training_data   = construct_tf_idf_matrix(data, store)
    print "... Training Matrix Size: %s x %s ..." % training_data.shape

    if run_diagnostics:
        import diagnostics
        diagnostics.find_best_parameters_for_SVM(training_data, training_labels)
    else:
        train(training_data, training_labels, store)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = """Train a multi-class classifier on BestBuy data and 
        predict the the most possible xbox game customer would click on the testing data.""")

    parser.add_argument('--store', action = 'store_true', default = True, help = 'Dump Important Data for Classifying Test Data.')
    parser.add_argument('--diagnostics', action = 'store_true', default = False, help = 'Run Diagnostics to Find Best Parameters.')

    args = vars(parser.parse_args())
    run(args['store'], args['diagnostics'])

