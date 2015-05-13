import directory

def write_prediction_result(predictions):

    print "... Writing predictions to: %s ..." % directory.TESTING_PREDICTIONS_FILE

    with open(directory.TESTING_PREDICTIONS_FILE, 'wb') as result_file:
        for row in predictions:
            result_file.write(','.join(str(value) for value in row) + '\n')

    print "... Writing Complete ..."