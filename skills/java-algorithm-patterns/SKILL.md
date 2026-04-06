---
name: java-algorithm-patterns
description: 5 algorithm patterns with full Java implementations for common coding problems
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Java algorithm patterns: Stream API, Binary Search, HashMap, Graph (JGraphT), Concurrent Collections"
    when_to_use: "When implementing algorithms, data structures, or solving coding problems in Java"
    quick_start: "Each pattern includes full implementation, complexity analysis, and key principles"
context_limit: 700
tags:
  - java
  - algorithms
  - stream-api
  - binary-search
  - hashmap
  - jgrapht
  - concurrent-collections
  - data-structures
  - complexity
requires_tools: []
---

# Java Algorithm Patterns

## Algorithm Patterns

### 1. Stream API Pattern (Functional Processing)
```java
// Pattern: Find longest substring without repeating characters
import java.util.*;
import java.util.stream.*;

public class StreamPatterns {
    /**
     * Find length of longest substring without repeating characters.
     * Uses Stream API for functional approach.
     * Time: O(n), Space: O(min(n, alphabet_size))
     *
     * Example: "abcabcbb" -> 3 (substring "abc")
     */
    public static int lengthOfLongestSubstring(String s) {
        if (s == null || s.isEmpty()) {
            return 0;
        }

        // Sliding window with HashMap tracking character positions
        Map<Character, Integer> charIndex = new HashMap<>();
        int maxLength = 0;
        int left = 0;

        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);

            // If character seen AND it's within current window
            if (charIndex.containsKey(c) && charIndex.get(c) >= left) {
                // Move left pointer past previous occurrence
                left = charIndex.get(c) + 1;
            }

            charIndex.put(c, right);
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }

    /**
     * Stream API example: Group and count elements
     * Time: O(n), Space: O(k) where k is unique elements
     */
    public static Map<String, Long> countFrequencies(List<String> items) {
        return items.stream()
            .collect(Collectors.groupingBy(
                item -> item,
                Collectors.counting()
            ));
    }

    // Stream API Key Principles:
    // 1. Functional pipeline: source -> intermediate ops -> terminal op
    // 2. Lazy evaluation: operations not executed until terminal op
    // 3. Collectors: groupingBy, partitioningBy, toMap, summarizingInt
    // 4. Parallel streams: Use .parallel() for CPU-bound operations on large datasets
    // 5. Avoid side effects: Don't modify external state in stream operations
}
```

### 2. Binary Search Pattern
```java
// Pattern: Binary search on sorted array
public class BinarySearchPatterns {
    /**
     * Find median of two sorted arrays in O(log(min(m,n))) time.
     *
     * Strategy: Binary search on smaller array to find partition point
     */
    public static double findMedianSortedArrays(int[] nums1, int[] nums2) {
        // Ensure nums1 is smaller for optimization
        if (nums1.length > nums2.length) {
            return findMedianSortedArrays(nums2, nums1);
        }

        int m = nums1.length;
        int n = nums2.length;
        int left = 0;
        int right = m;

        while (left <= right) {
            int partition1 = (left + right) / 2;
            int partition2 = (m + n + 1) / 2 - partition1;

            // Handle edge cases with infinity
            int maxLeft1 = (partition1 == 0) ? Integer.MIN_VALUE : nums1[partition1 - 1];
            int minRight1 = (partition1 == m) ? Integer.MAX_VALUE : nums1[partition1];

            int maxLeft2 = (partition2 == 0) ? Integer.MIN_VALUE : nums2[partition2 - 1];
            int minRight2 = (partition2 == n) ? Integer.MAX_VALUE : nums2[partition2];

            // Check if partition is valid
            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                // Found correct partition
                if ((m + n) % 2 == 0) {
                    return (Math.max(maxLeft1, maxLeft2) + Math.min(minRight1, minRight2)) / 2.0;
                }
                return Math.max(maxLeft1, maxLeft2);
            } else if (maxLeft1 > minRight2) {
                right = partition1 - 1;
            } else {
                left = partition1 + 1;
            }
        }

        throw new IllegalArgumentException("Input arrays must be sorted");
    }

    // Binary Search Key Principles:
    // 1. Sorted data: Binary search requires sorted input
    // 2. Divide and conquer: Eliminate half of search space each iteration
    // 3. Time complexity: O(log n) vs O(n) linear search
    // 4. Edge cases: Empty arrays, single elements, duplicates
    // 5. Integer overflow: Use left + (right - left) / 2 instead of (left + right) / 2
}
```

### 3. HashMap Pattern (O(1) Lookup)
```java
// Pattern: Two sum problem with HashMap
import java.util.*;

public class HashMapPatterns {
    /**
     * Find indices of two numbers that sum to target.
     * Time: O(n), Space: O(n)
     */
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();

        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {
                return new int[] { seen.get(complement), i };
            }
            seen.put(nums[i], i);
        }

        return new int[] {}; // No solution found
    }

    // HashMap Key Principles:
    // 1. O(1) lookup: Convert O(n^2) nested loops to O(n) single pass
    // 2. Trade space for time: Use memory to store seen values
    // 3. Hash function: Good distribution prevents collisions
    // 4. Load factor: Default 0.75 balances time vs space
    // 5. ConcurrentHashMap: Use for thread-safe operations
}
```

### 4. Graph Algorithms (JGraphT)
```java
// Pattern: Shortest path using JGraphT
import org.jgrapht.*;
import org.jgrapht.alg.shortestpath.*;
import org.jgrapht.graph.*;
import java.util.*;

public class GraphPatterns {
    /**
     * Find shortest path in weighted graph using Dijkstra.
     * Time: O((V + E) log V) with binary heap
     */
    public static List<String> findShortestPath(
            Graph<String, DefaultWeightedEdge> graph,
            String source,
            String target
    ) {
        DijkstraShortestPath<String, DefaultWeightedEdge> dijkstra =
            new DijkstraShortestPath<>(graph);

        GraphPath<String, DefaultWeightedEdge> path = dijkstra.getPath(source, target);

        return path != null ? path.getVertexList() : Collections.emptyList();
    }

    /**
     * Create directed weighted graph
     */
    public static Graph<String, DefaultWeightedEdge> createGraph() {
        Graph<String, DefaultWeightedEdge> graph =
            new DefaultDirectedWeightedGraph<>(DefaultWeightedEdge.class);

        // Add vertices
        graph.addVertex("A");
        graph.addVertex("B");
        graph.addVertex("C");

        // Add weighted edges
        DefaultWeightedEdge edge = graph.addEdge("A", "B");
        graph.setEdgeWeight(edge, 5.0);

        return graph;
    }

    // Graph Algorithm Key Principles:
    // 1. JGraphT library: Production-ready graph algorithms
    // 2. Dijkstra: Shortest path in weighted graphs (non-negative weights)
    // 3. BFS: Shortest path in unweighted graphs
    // 4. DFS: Cycle detection, topological sort
    // 5. Time complexity: Consider |V| + |E| for graph operations
}
```

### 5. Concurrent Collections Pattern
```java
// Pattern: Thread-safe collections for concurrent access
import java.util.concurrent.*;
import java.util.*;

public class ConcurrentPatterns {
    /**
     * Thread-safe queue for producer-consumer pattern.
     * BlockingQueue handles synchronization automatically.
     */
    public static class ProducerConsumer {
        private final BlockingQueue<String> queue = new LinkedBlockingQueue<>(100);

        public void produce(String item) throws InterruptedException {
            queue.put(item); // Blocks if queue is full
        }

        public String consume() throws InterruptedException {
            return queue.take(); // Blocks if queue is empty
        }
    }

    /**
     * Thread-safe map with atomic operations.
     * ConcurrentHashMap provides better concurrency than synchronized HashMap.
     */
    public static class ConcurrentCache {
        private final ConcurrentHashMap<String, String> cache = new ConcurrentHashMap<>();

        public String getOrCompute(String key) {
            return cache.computeIfAbsent(key, k -> expensiveComputation(k));
        }

        private String expensiveComputation(String key) {
            // Simulated expensive operation
            return "computed_" + key;
        }
    }

    // Concurrent Collections Key Principles:
    // 1. ConcurrentHashMap: Lock striping for better concurrency than synchronized
    // 2. BlockingQueue: Producer-consumer with automatic blocking
    // 3. CopyOnWriteArrayList: For read-heavy, write-rare scenarios
    // 4. Atomic operations: computeIfAbsent, putIfAbsent, merge
    // 5. Lock-free algorithms: Better scalability than synchronized blocks
}
```
