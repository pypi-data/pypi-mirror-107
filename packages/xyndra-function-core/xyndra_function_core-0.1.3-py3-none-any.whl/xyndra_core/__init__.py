import numpy as np

def arr_to_p_and_s_raw(arr1):

    arr2 = [0.0 for i in range(len(list(dict.fromkeys(arr1))))]
    arr3 = list(set(arr1))
    for x in arr1:
        arr2[arr3.index(x)] = arr2[arr3.index(x)]+1/len(arr1)
    
    return arr2, arr3

def arr_to_p_and_s(arr1):

    arr2 = [0.0 for i in range(len(list(dict.fromkeys(arr1))))]
    arr3 = list(set(arr1))
    for x in arr1:
        arr2[arr3.index(x)] = arr2[arr3.index(x)]+1/len(arr1)
    
    a, b = sort_p_and_s(arr2, arr3)

    return a, b

def sort_p_and_s(arr1, arr2):
    arr3 = []
    arr4 = []

    for i in range(len(arr1)):
        max = np.argmax(arr1)
        arr3.append(arr1[max])
        del arr1[max]
        arr4.append(arr2[max])
    
    return arr3, arr4
