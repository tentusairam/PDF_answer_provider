
n = int(input("Enter the number of terms: "))

a = 0
b = 1
count = 0
c=1

while count < n:
    print(a, end=" ")
    c = a + b
    a = b
    b = c
    c+=1
    count += 1
print("\nnumber of iterations:", count)
print(c)