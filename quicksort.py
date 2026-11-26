

count = 0

def quicksort(arr):
    global count

    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    left = []
    right = []

    for i in arr[1:]:
        count += 1

        if i <= pivot:
            left.append(i)
        else:
            right.append(i)

    return quicksort(left) + [pivot] + quicksort(right)


arr = list(map(int, input("Enter array elements: ").split()))

sorted_arr = quicksort(arr)

print("Sorted Array:", sorted_arr)
print("Number of Iterations:", count)
