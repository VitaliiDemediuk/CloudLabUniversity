import math
from Pyro4 import expose

def mergeSort(array):
    if len(array) > 1:

        r = len(array) // 2
        L = array[:r]
        R = array[r:]

        mergeSort(L)
        mergeSort(R)

        merge(array, L, R)


def merge(res, arr1, arr2):
    assert(len(res) == len(arr1) + len(arr2))

    i = j = k = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            res[k] = arr1[i]
            i += 1
        else:
            res[k] = arr2[j]
            j += 1
        k += 1

    while i < len(arr1):
        res[k] = arr1[i]
        i += 1
        k += 1

    while j < len(arr2):
        res[k] = arr2[j]
        j += 1
        k += 1

class Solver:

    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers


    def solve(self):
        work_count = len(self.workers)

        input_list = self.read_input()

        chunks = self.get_chunks(input_list, work_count)

        mapped = list()
        for i in xrange(0, work_count):
            mapped.append(self.workers[i].mymap(chunks[i]))

        reduced = self.myreduce(mapped)

        self.write_output(reduced)


    @staticmethod
    @expose
    def myreduce(mapped):
        mapped_lists = list()

        for x in mapped:
            mapped_lists.append(x.value)

        while len(mapped_lists) > 1:
            tmp = list()

            for i in xrange(0, len(mapped_lists), 2):
                if i != len(mapped_lists) - 1:
                    new_list = [None] * (len(mapped_lists[i]) + len(mapped_lists[i+1]))
                    merge(new_list, mapped_lists[i], mapped_lists[i+1])
                    tmp.append(new_list)
                else:
                    new_list = [None] * (len(mapped_lists[i]) + len(tmp[-1]))
                    merge(new_list, mapped_lists[i], tmp[-1])
                    tmp[-1] = new_list

            mapped_lists = tmp

        return mapped_lists[0]


    @staticmethod
    def get_chunks(lst, n):
        res = list()

        d, r = divmod(len(lst), n)
        for i in range(n):
            si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
            res.append(lst[si:si+(d+1 if i < r else d)])

        return res


    def read_input(self):
        res = list()
        with open(self.input_file_name, 'r') as in_file:
            for line in in_file:
                res.append(int(line))
        return res


    def write_output(self, out_list):
        with open(self.output_file_name, 'w') as in_file:
            for n in out_list:
                in_file.write(str(n) + "\n")


    @staticmethod
    @expose
    def mymap(chunk):
        mergeSort(chunk)
        return chunk