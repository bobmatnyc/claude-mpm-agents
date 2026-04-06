---
name: python-algorithm-cookbook
description: 4 algorithm patterns with full Python implementations for common coding problems
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "4 algorithm patterns: sliding window, BFS traversal, binary search, and hash map with full implementations"
    when_to_use: "When implementing algorithms for coding problems or optimizing data processing"
    quick_start: "Match your problem type to the right pattern: substring constraints -> sliding window, tree/graph -> BFS, sorted data -> binary search, O(1) lookup -> hash map"
context_limit: 700
tags:
  - python
  - algorithms
  - sliding-window
  - bfs
  - binary-search
  - hash-map
  - two-pointers
  - data-structures
  - complexity
requires_tools: []
---

# Common Algorithm Patterns

## Sliding Window (Two Pointers)

```python
# Pattern: Longest Substring Without Repeating Characters
def length_of_longest_substring(s: str) -> int:
    """Find length of longest substring without repeating characters.

    Sliding window technique with hash map to track character positions.
    Time: O(n), Space: O(min(n, alphabet_size))

    Example: "abcabcbb" -> 3 (substring "abc")
    """
    if not s:
        return 0

    # Track last seen index of each character
    char_index: dict[str, int] = {}
    max_length = 0
    left = 0  # Left pointer of sliding window

    for right, char in enumerate(s):
        # If character seen AND it's within current window
        if char in char_index and char_index[char] >= left:
            # Move left pointer past the previous occurrence
            # This maintains "no repeating chars" invariant
            left = char_index[char] + 1

        # Update character's latest position
        char_index[char] = right

        # Update max length seen so far
        # Current window size is (right - left + 1)
        max_length = max(max_length, right - left + 1)

    return max_length

# Sliding Window Key Principles:
# 1. Two pointers: left (start) and right (end) define window
# 2. Expand window by incrementing right pointer
# 3. Contract window by incrementing left when constraint violated
# 4. Track window state with hash map, set, or counter
# 5. Update result during expansion or contraction
# Common uses: substring/subarray with constraints (unique chars, max sum, min length)
```

## BFS Tree Traversal (Level Order)

```python
# Pattern: Binary Tree Level Order Traversal (BFS)
from collections import deque
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def level_order_traversal(root: Optional[TreeNode]) -> list[list[int]]:
    """Perform BFS level-order traversal of binary tree.

    Returns list of lists where each inner list contains node values at that level.
    Time: O(n), Space: O(w) where w is max width of tree

    Example:
        Input:     3
                  / \
                 9  20
                   /  \
                  15   7
        Output: [[3], [9, 20], [15, 7]]
    """
    if not root:
        return []

    result: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        # CRITICAL: Capture level size BEFORE processing
        # This separates current level from next level nodes
        level_size = len(queue)
        current_level: list[int] = []

        # Process exactly level_size nodes (all nodes at current level)
        for _ in range(level_size):
            node = queue.popleft()  # O(1) with deque
            current_level.append(node.val)

            # Add children for next level processing
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result

# BFS Key Principles:
# 1. Use collections.deque for O(1) append/popleft operations (NOT list)
# 2. Capture level_size = len(queue) before inner loop to separate levels
# 3. Process entire level before moving to next (prevents mixing levels)
# 4. Add children during current level processing
# Common uses: level order traversal, shortest path, connected components, graph exploration
```

## Binary Search on Two Arrays

```python
# Pattern: Median of two sorted arrays
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """Find median of two sorted arrays in O(log(min(m,n))) time.

    Strategy: Binary search on smaller array to find partition point
    """
    # Ensure nums1 is smaller for optimization
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1

        # Handle edge cases with infinity
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]

        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]

        # Check if partition is valid
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found correct partition
            if (m + n) % 2 == 0:
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
            return max(max_left1, max_left2)
        elif max_left1 > min_right2:
            right = partition1 - 1
        else:
            left = partition1 + 1

    raise ValueError("Input arrays must be sorted")
```

## Hash Map for O(1) Lookup

```python
# Pattern: Two sum problem
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Find indices of two numbers that sum to target.

    Time: O(n), Space: O(n)
    """
    seen: dict[int, int] = {}

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i

    return None
```

## When to Use Each Pattern

- **Sliding Window**: Substring/subarray with constraints (unique chars, max/min sum, fixed/variable length)
- **BFS with Deque**: Tree/graph level-order traversal, shortest path, connected components
- **Binary Search on Two Arrays**: Median, kth element in sorted arrays (O(log n))
- **Hash Map**: O(1) lookups to convert O(n^2) nested loops to O(n) single pass
