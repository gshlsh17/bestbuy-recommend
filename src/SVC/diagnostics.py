def _purge_classes_with_too_few_members(training_data, training_labels, minimum):

    import numpy
    import scipy.sparse
    
    print "Purging samples of classes with < %s members" % minimum

    # for iteration.
    training_data = training_data.todok()

    # count first.
    frequencies = dict()
    for value in training_labels:
        if value not in frequencies:
            frequencies[value] = 0
        frequencies[value] += 1

    usable_samples = sum(frequencies[key] for key in frequencies if frequencies[key] >= minimum)

    print "Leaving %s samples from %s classes" % (usable_samples,
        sum(1 for key in frequencies if frequencies[key] >= minimum))

    new_training_data = scipy.sparse.dok_matrix((usable_samples, training_data.shape[1]),
        dtype=training_data.dtype)

    new_training_labels = numpy.zeros(shape=(usable_samples), dtype=training_labels.dtype)

    row_counter = 0
    for i in xrange(training_data.shape[0]):
        if frequencies[training_labels[i]] >= minimum:
            for j in xrange(new_training_data.shape[1]):
                new_training_data[row_counter, j] = training_data[i, j]
            new_training_labels[row_counter] = training_labels[i]
            row_counter += 1

    print "Purging Complete"
    # for fast arithmetic ops
    return new_training_data.tocsr(), new_training_labels


def find_best_parameters_for_SVM(training_data, training_labels, verbose=False):

    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import SVC

    classifier = SVC(kernel='poly')

    parameters = {'tol' : [1e-3, 1e-4, 1e-5], 
        'C': [0.01, 0.1, 0.2, 0.4, 0.8, 1, 2, 4, 8, 16],
        'degree': [1, 2, 3, 4, 5, 6, 7],
        'gamma': [0.0, 0.5, 1.0, 5.0],
        'coef0': [0.0, 0.1, 0.5, 1.0, 5.0]
    }

    grd = GridSearchCV(classifier, parameters, cv=3, n_jobs=-1)
    new_training_data, new_training_labels = \
        _purge_classes_with_too_few_members(training_data, training_labels, grd.cv)

    print "Grid Parameters: %s" % parameters
    print "Starting Grid Search..."
    grd.fit(new_training_data, new_training_labels)

    print "Best: ", grd.best_params_
    print "Scores: ", grd.grid_scores_

    print "Done Grid Searching."
