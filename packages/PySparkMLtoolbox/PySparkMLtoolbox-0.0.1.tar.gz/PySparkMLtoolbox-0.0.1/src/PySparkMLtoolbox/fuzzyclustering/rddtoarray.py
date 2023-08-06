import dataito

def rddtoarray_float(data):
    data = data.collect()
    data = dataito.transform(data,'array')
    data = data.astype(float)

    return data