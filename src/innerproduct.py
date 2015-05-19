import xml.etree.ElementTree as ET
import csv
import sys
from collections import defaultdict
from Parser import *
import operator
from preprocess import *
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
from numpy import *
from heapq import *
import re
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
import time

def getProductInfo():
    productTree = ET.parse('../data/small_product_data.xml')
    root = productTree.getroot()
    productSkus = []
    productDescpt = []
    for product in root.findall('product'):
        sku = product.find('sku').text
        description = product.find('longDescription').text
        productSkus.append(sku)
        productDescpt.append(description)
    return productSkus, productDescpt

def getDatumInfo(testFileName):    
    testFile = open(testFileName, 'r')
    reader = csv.reader(testFile)
    datum = []
    queries = []
    for row in reader:
        datum.append(row)
        queries.append(row[3])
    return datum, queries

if __name__ == "__main__":
    mod = SourceModule("""
        #define N 1024
      __global__ void getScore(float *res, float *a, float *b)
      {
        __shared__ float temp[N];
        int idx = blockIdx.x * 1024 + threadIdx.x;
        if(idx < 9718)
            temp[threadIdx.x] = a[idx] * b[idx];
        __syncthreads(); 
        if( 0 == threadIdx.x ) {
            float sum = 0;
            for( int i = 0; i < N; i++ )
            sum += temp[i];
            res[blockIdx.x] = sum;
        }
      }
      """)
    func = mod.get_function("getScore")

    testFileName = '../data/psudo_test2.csv'
    productSkus, productDescpt = getProductInfo()
    datum, queries = getDatumInfo(testFileName)
    corpus = []
    corpus.extend(productDescpt)
    corpus.extend(queries)

    vectorizer = TfidfVectorizer(min_df=1)
    tfidf = vectorizer.fit_transform(corpus)
    tfidfArray = tfidf.toarray()
    numProducts = len(productSkus)
    numQuery = len(datum)
    tfidfArray = tfidfArray.astype(numpy.float32)


    """
    for each query, I get the top five sku with product(tfidf(product), tfidf(query))
    """
    vectorLen = len(tfidfArray[0])
    start1 = time.clock()
    # normal version
    for x in range(0, 10):
        trueSku = datum[x][1]
        query = queries[x]
        #first do content-based filtering
        queryArray = tfidfArray[x+numProducts,:]
        scoreDict = {}
        for j in range(0, numProducts):
            prodArray = tfidfArray[j,:]
            score1 = 0.0
            for i in range(vectorLen):
                score1 += queryArray[i] * prodArray[i]

    end1 = time.clock()

    start2 = time.clock()
    # GPU version
    for x in range(0, 10):
        trueSku = datum[x][1]
        query = queries[x]
        #first do content-based filtering
        queryArray = tfidfArray[x+numProducts,:]
        scoreDict = {}
        for j in range(0, numProducts):
            prodArray = tfidfArray[j,:]
            score2 = 0.0
            res = numpy.zeros(10, dtype=numpy.float32)
            func(cuda.Out(res), cuda.In(queryArray), cuda.In(prodArray), block=(1024, 1, 1) , grid=(10,1,1))
            for s in res:
                score2 += s

    end2 = time.clock()


    print 'Running time for GPU programming:    ' + str(end2 - start2)
    print 'Running time for normal programming: ' + str(end1 - start1)





