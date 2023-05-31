import numpy as np
import threading
import time
import sys
import multiprocessing

result = []


def selectSamples(A, k, p):
    samples = np.random.choice(A, size=p*k, replace=True)
    samples.sort()
    splitters = np.empty(p+1)
    splitters[0] = -np.inf
    splitters[p] = np.inf
    for i in range(1, p):
        splitters[i] = samples[i*k]
    # print(splitters, len(splitters))
    return splitters


def placeInBuckets(A, splitters):
    buckets = [[] for _ in range(len(splitters)-1)]
    for a in A:
        j = np.searchsorted(splitters, a, side='right') - 1
        if j < len(buckets):
            buckets[j].append(a)
    # print("bucket", buckets)
    return buckets


def sampleSortThread(bucket, i):
    print(i)
    chunk = np.sort(bucket, kind='mergesort')
    result.extend(chunk)


def sampleSort(A, k=10, p=8):
    A = np.array(A)
    splitters = selectSamples(A, k, p)
    buckets = placeInBuckets(A, splitters)

    threads = []
    for i in range(len(buckets)):
        thread = threading.Thread(
            target=sampleSortThread, args=(buckets[i], i))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 GigaSort.py <inputPath> <outputPath>")
        return

    path_in = sys.argv[1]
    path_out = sys.argv[2]

    start_time_avx = time.time()
    values = []
    keys = []
    # path_in = 'data/input/sort-rand-199999999.txt'
    # lines = read_file_parallel('data/input/sort-rand-199999999.txt')
    f = open(path_in, "r")
    count = 0
    for line in f:
        # if count == 2000:
        #     break
        line = line.replace("\n", "")
        a, b = line.split(" ")
        keys.append(a)
        values.append(float(b))
        # print(num)
        count += 1
    # print(arr)
    # for i in range(count):
    #     num = float(f.readline().replace("\n", "").split(" ")[1])
    #     arr.append(num)

    # Time the NumPy sort function
    # start_time_np = time.time()
    # sorted_arr_np = sampleSort(arr)
    # end_time_np = time.time()
    # print("test sort time:", end_time_np - start_time_np)
    # print(result)

    # Time the AVX sort function
    # start_time_avx = time.time()
    # sorted_arr_avx = np.sort(arr)
    # print(sorted_arr_avx)
    arr = np.array(values)
    # key = np.array(keys)
    indices_arr = np.argsort(arr, kind='mergesort')
    # keyout = key[indices_arr]
    # valout = arr[indices_arr]
    # print(key[indices_arr])
    # print(arr[indices_arr])
    # sorted_arr_avx = sort_and_merge_chunks(arr)
    # end_time_avx = time.time()
    # print("numpy sort time:", end_time_avx - start_time_avx)

    # Verify that the two arrays are the same
    # assert np.allclose(sorted_arr_np, sorted_arr_avx)

    # path_out = 'data/output/output.txt'
    file_output = open(path_out, "w")
    for i in range(count):
        file_output.write(keys[indices_arr[i]]+' ' +
                          str(arr[indices_arr[i]])+'\n')
    file_output.close()

    end_time_avx = time.time()
    print("usage time:", end_time_avx - start_time_avx)


if __name__ == '__main__':
    main()

# python gigaSort.py data/input/sort-rand-199999999.txt data/output/output.txt
# docker run -v "$(pwd)"/data/input:/input -v "$(pwd)"/data/output:/output gigasort /input/sort-rand-199999999.txt /output/output.txt

# time docker run -v "$(pwd)"/data/input:/input -v "$(pwd)"/data/output:/output watcharavit/high-performance-arch:gigasort ./prog /input/sort-rand-199999999.txt /output/output.txt
