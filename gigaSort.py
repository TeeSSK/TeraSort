import queue
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import numexpr as ne


def mergesort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])

    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result += right[j:]
    return result


def merge_sorted_chunks(sorted_chunks):
    # Create a priority queue to store the next element from each sorted chunk
    pq = queue.PriorityQueue()
    for i, chunk in enumerate(sorted_chunks):
        if len(chunk) > 0:
            pq.put((chunk[0], i, 0))

    # Merge the chunks using a priority queue-based algorithm
    result = []
    while not pq.empty():
        val, array_idx, element_idx = pq.get()
        result.append(val)
        if element_idx + 1 < len(sorted_chunks[array_idx]):
            pq.put((sorted_chunks[array_idx]
                   [element_idx+1], array_idx, element_idx+1))

    return result


def sort_chunk(arr):
    # Sort a chunk of the input array
    return np.sort(arr)


def sort_and_merge_chunks(input_data, num_threads=4, k=4):
    # Split the input data into chunks for multi-threading
    chunk_size = len(input_data) // num_threads
    chunks = [input_data[i:i+chunk_size]
              for i in range(0, len(input_data), chunk_size)]

    # Sort each chunk in parallel using separate threads
    sorted_chunks = []
    threads = []
    for chunk in chunks:
        t = threading.Thread(target=lambda c: sorted_chunks.append(
            sort_chunk(c)), args=(chunk,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Merge the sorted chunks using a k-way merge algorithm
    while len(sorted_chunks) > k:
        new_sorted_chunks = []
        for i in range(0, len(sorted_chunks), k):
            chunk = sorted_chunks[i:i+k]
            new_sorted_chunks.append(merge_sorted_chunks(chunk))
        sorted_chunks = new_sorted_chunks

    sorted_data = merge_sorted_chunks(sorted_chunks)
    return sorted_data


def main():
    arr = []
    f = open("sort-rand-199999999.txt", "r")
    # lines = f.readlines()
    count = 0
    for line in f:
        if count == 10000000:
            break
        line = line.replace("\n", "")
        num = float(line.split(" ")[1])
        # print(num)
        arr.append(num)
        # print(line)
        count += 1
    # for i in range(count):
    #     num = float(f.readline().replace("\n", "").split(" ")[1])
    #     arr.append(num)

    # Time the NumPy sort function
    start_time_np = time.time()
    sorted_arr_np = np.sort(arr, kind='mergesort')
    end_time_np = time.time()
    print("NumPy sort time:", end_time_np - start_time_np)

    # Time the AVX sort function
    start_time_avx = time.time()
    # sorted_arr_avx = np.sort(arr, kind='mergesort')
    sorted_arr_avx = sort_and_merge_chunks(arr)
    end_time_avx = time.time()
    print("test sort time:", end_time_avx - start_time_avx)

    # Verify that the two arrays are the same
    # assert np.allclose(sorted_arr_np, sorted_arr_avx)


if __name__ == '__main__':
    main()
