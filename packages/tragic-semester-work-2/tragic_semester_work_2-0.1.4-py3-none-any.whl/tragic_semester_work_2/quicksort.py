import random


def quicksort(nums):
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
    l_nums = [n for n in nums if n < q]

    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n > q]
    return quicksort(l_nums) + e_nums + quicksort(b_nums)


def main():
    arr = [10, 7, 8, 9, 1, 5]
    print("Sorted array is:")
    print(quicksort(arr))


if __name__ == '__main__':
    main()
