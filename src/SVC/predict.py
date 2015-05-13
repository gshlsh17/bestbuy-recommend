import directory
import numpy
import pickle
import load
import dump
import argparse



def construct_tf_idf_matrix(data):
    print "... Loading TF-IDF Transforming data ..." 
    transformer      = pickle.load(open(directory.TFIDF_FILE, 'rb'))
    transformed_data = transformer.transform(data)
    print "... TF-IDF Transformation Complete ..."

    return transformed_data


def do_prediction(data, number_of_predictions):
    print "... Load Classifier data ..." 
    classifier = pickle.load(open(directory.CLASSIFIER__FILE, 'rb'))

    print "... Load label & sku mapping data ..."
    label_sku_mapping = pickle.load(open(directory.LABEL_SKU_MAPPING_FILE, 'rb'))

    if number_of_predictions > len(label_sku_mapping):
        raise Exception("... Too many predictions requested ...")

    predictions = classifier.predict_proba(data)

    predictions_top = numpy.zeros(shape=(data.shape[0], number_of_predictions), dtype=numpy.uint64)

    for i in xrange(predictions.shape[0]):
        values = dict( ( (value, j) for j, value in enumerate(predictions[i]) ) )
        sorted_keys = sorted(values.keys(), reverse=True)

        for j in xrange(number_of_predictions):
            prediction = values[sorted_keys[j]]
            predictions_top[i, j] = label_sku_mapping[prediction]

    return predictions_top


def run(number_of_predictions):
    print "... Number of Predictions: %s ..." % number_of_predictions

    origin_testing_data = load.loadTestingData()
    print "... Number of Testing Data Points: %s ..." % len(origin_testing_data)

    testing_data = construct_tf_idf_matrix(origin_testing_data)
    print "... Testing Matrix size: %s x %s ..." % testing_data.shape

    prediction_data = do_prediction(testing_data, number_of_predictions)
    print "... Prediction for Testing Data Complete ..."



    dump.write_prediction_result(prediction_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Predict the most likely labels
        for each record in the testing set. """)

    parser.add_argument('-predictions', type=int, default=5,
        help='Number of predictions for record to make.')

    args = vars(parser.parse_args())
    run(args['predictions'])
