def check(stones, p, k):
    # p명이 지나갈 수 있는가?
    after_walk = [stone - p for stone in stones]

    cnt = 0
    for num in after_walk:
        if num <= 0:
            cnt += 1

            if cnt > k:
                return False
        else:
            cnt = 0
    
    return True


def solution(stones, k):
    max_p = max(stones)
    min_p = min(stones)

    while max_p > min_p:
        mid_p = (max_p + min_p) // 2

        if check(stones, mid_p, k):
            min_p = mid_p
        else:
            max_p = mid_p - 1
    
    return max_p

stones = [2, 4, 5, 3, 2, 1, 4, 2, 5, 1]
k = 3

print(solution(stones, k))