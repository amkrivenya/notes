from typing import List

a = [3,6,6,5,3,99,77,55,8,9,1,2,3,4,5]

print (a)

def shell_sort(data: List[int]):

    last_index = len(data)
    step = len(data)//2
    while step > 0:
        for i in range(step, last_index, 1):
            j = i
            delta = j - step
            while delta >= 0 and data[delta] > data[j]:
                data[delta], data[j] = data[j], data[delta]
                j = delta
                delta = j - step
                print(data)
        step //= 2
    return data

shell_sort(a)
print(a)