import codecs
import directory


def transformTimeString(raw_string, identifier):
    year, month, day = raw_string.split('-')

    year += '_' + identifier + '_year'
    month += '_' + identifier + '_month'
    day += '_' + identifier + '_day'

    return year + ' ' + month + ' ' + day



def loadTrainingData():
    return loadData(directory.TRAINING_DATA_FILE, training_data = True)



def loadTestingData():
    return loadData(directory.TESTING_DATA_FILE, training_data = False)



def loadData(data_file, training_data = True):
    print "... Loading data from: %s ..." % data_file
    
    skus = None
    if training_data:
        skus = list()


    data = list()

    # read in data.
    with codecs.open(data_file, encoding='utf-8', mode='rb') as reader:
        #reader.next()   # skip the header

        for row in reader:
            if training_data:
                _, sku, category, query, click_timestamp, query_timestamp = row.split(',')
            else:
                _, _, category, query, click_timestamp, query_timestamp = row.split(',')


            if training_data:
                skus.append(int(sku))

            datum = category + ' ' +  query
            click_date, click_time = click_timestamp.split()
            query_date, query_time = query_timestamp.split()
            datum += ' ' + transformTimeString(click_date, 'click')
            datum += ' ' + transformTimeString(query_date, 'query')
            data.append(datum)

    if training_data:
        return data, skus
    else:
        return data
