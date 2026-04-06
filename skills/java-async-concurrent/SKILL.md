---
name: java-async-concurrent
description: 5 async/concurrent patterns with full Java implementations for high-performance systems
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Java async/concurrent patterns: Virtual Threads, CompletableFuture, Reactive Streams, Thread Pool, Resilience4j"
    when_to_use: "When implementing concurrent, async, or resilient systems in Java 21+"
    quick_start: "Each pattern includes full implementation, key principles, and when to use vs alternatives"
context_limit: 700
tags:
  - java
  - async
  - concurrent
  - virtual-threads
  - completable-future
  - reactive
  - project-reactor
  - thread-pool
  - resilience4j
  - retry
requires_tools: []
---

# Java Async/Concurrent Patterns

## Async/Concurrent Patterns

### 1. Virtual Threads (Java 21)
```java
// Pattern: Virtual threads for high concurrency
import java.time.*;
import java.util.concurrent.*;
import java.util.*;

public class VirtualThreadPatterns {
    /**
     * Process tasks concurrently using virtual threads.
     * Virtual threads are lightweight (millions possible) and perfect for I/O.
     *
     * Key Difference from Platform Threads:
     * - Platform threads: ~1MB stack, thousands max, pooled with ExecutorService
     * - Virtual threads: ~1KB stack, millions possible, no pooling needed
     */
    public static <T> List<T> processConcurrentTasks(
            List<Callable<T>> tasks,
            Duration timeout
    ) throws InterruptedException, ExecutionException, TimeoutException {
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            List<Future<T>> futures = executor.invokeAll(
                tasks,
                timeout.toMillis(),
                TimeUnit.MILLISECONDS
            );

            List<T> results = new ArrayList<>();
            for (Future<T> future : futures) {
                if (!future.isCancelled()) {
                    results.add(future.get()); // May throw ExecutionException
                }
            }

            return results;
        }
    }

    /**
     * Create virtual thread directly (Java 21+)
     */
    public static void runAsyncTask(Runnable task) {
        Thread.startVirtualThread(task);
    }

    // Virtual Threads Key Principles:
    // 1. Use for I/O-bound workloads (network calls, database queries)
    // 2. Don't use for CPU-bound workloads (use platform threads or ForkJoinPool)
    // 3. Don't pool virtual threads (they're cheap to create)
    // 4. Avoid synchronized blocks (use ReentrantLock instead to prevent pinning)
    // 5. Use ExecutorService with try-with-resources for automatic shutdown
}
```

### 2. CompletableFuture Pattern
```java
// Pattern: CompletableFuture for async operations with error handling
import java.util.concurrent.*;
import java.time.*;
import java.util.*;
import java.util.stream.*;

public class CompletableFuturePatterns {
    /**
     * Execute async operations with timeout and error handling.
     * CompletableFuture provides functional composition of async tasks.
     */
    public static <T> CompletableFuture<T> withTimeout(
            Supplier<T> operation,
            Duration timeout
    ) {
        return CompletableFuture.supplyAsync(operation)
            .orTimeout(timeout.toMillis(), TimeUnit.MILLISECONDS)
            .exceptionally(ex -> {
                // Handle both timeout and other exceptions
                if (ex instanceof TimeoutException) {
                    throw new RuntimeException("Operation timed out", ex);
                }
                throw new RuntimeException("Operation failed", ex);
            });
    }

    /**
     * Combine multiple async operations (equivalent to Promise.all)
     */
    public static <T> CompletableFuture<List<T>> allOf(
            List<CompletableFuture<T>> futures
    ) {
        return CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
            .thenApply(v -> futures.stream()
                .map(CompletableFuture::join)
                .collect(Collectors.toList())
            );
    }

    /**
     * Chain async operations with error recovery
     */
    public static CompletableFuture<String> chainedOperations() {
        return CompletableFuture.supplyAsync(() -> "initial")
            .thenApply(String::toUpperCase)
            .thenCompose(s -> CompletableFuture.supplyAsync(() -> s + "_PROCESSED"))
            .exceptionally(ex -> "FALLBACK_VALUE");
    }

    // CompletableFuture Key Principles:
    // 1. Async by default: supplyAsync runs on ForkJoinPool.commonPool()
    // 2. Composition: thenApply (sync), thenCompose (async), thenCombine
    // 3. Error handling: exceptionally, handle, whenComplete
    // 4. Timeout: orTimeout (Java 9+), completeOnTimeout
    // 5. Join vs Get: join() throws unchecked, get() throws checked exceptions
}
```

### 3. Reactive Streams (Project Reactor)
```java
// Pattern: Reactive programming with Project Reactor
import reactor.core.publisher.*;
import reactor.core.scheduler.*;
import java.time.Duration;
import java.util.*;

public class ReactivePatterns {
    /**
     * Process stream of data with backpressure handling.
     * Flux is for 0..N elements, Mono is for 0..1 element.
     */
    public static Flux<String> processStream(
            Flux<String> input,
            int concurrency
    ) {
        return input
            .flatMap(
                item -> Mono.fromCallable(() -> processItem(item))
                    .subscribeOn(Schedulers.boundedElastic()), // Non-blocking I/O
                concurrency // Control parallelism
            )
            .onErrorContinue((error, item) -> {
                // Continue processing on error, don't fail entire stream
                System.err.println("Failed to process: " + item + ", error: " + error);
            })
            .timeout(Duration.ofSeconds(10)); // Timeout per item
    }

    /**
     * Retry with exponential backoff
     */
    public static <T> Mono<T> retryWithBackoff(
            Mono<T> operation,
            int maxRetries
    ) {
        return operation.retryWhen(
            Retry.backoff(maxRetries, Duration.ofMillis(100))
                .maxBackoff(Duration.ofSeconds(5))
                .filter(throwable -> throwable instanceof RuntimeException)
        );
    }

    private static String processItem(String item) {
        // Simulate processing
        return "processed_" + item;
    }

    // Reactive Streams Key Principles:
    // 1. Backpressure: Subscriber controls flow, prevents overwhelming
    // 2. Non-blocking: Use Schedulers.boundedElastic() for I/O operations
    // 3. Error handling: onErrorContinue, onErrorResume, retry
    // 4. Hot vs Cold: Cold streams replay for each subscriber
    // 5. Operators: flatMap (async), map (sync), filter, reduce, buffer
}
```

### 4. Thread Pool Pattern (Traditional)
```java
// Pattern: Thread pool configuration for CPU-bound tasks
import java.util.concurrent.*;
import java.time.Duration;
import java.util.*;

public class ThreadPoolPatterns {
    /**
     * Create optimized thread pool for CPU-bound tasks.
     * For I/O-bound tasks, use virtual threads instead.
     */
    public static ExecutorService createCpuBoundPool() {
        int cores = Runtime.getRuntime().availableProcessors();

        return new ThreadPoolExecutor(
            cores,                          // Core pool size
            cores,                          // Max pool size (same for CPU-bound)
            60L, TimeUnit.SECONDS,         // Keep-alive time
            new LinkedBlockingQueue<>(100), // Bounded queue prevents memory issues
            new ThreadPoolExecutor.CallerRunsPolicy() // Rejection policy
        );
    }

    /**
     * Create thread pool for I/O-bound tasks (legacy, use virtual threads instead).
     */
    public static ExecutorService createIoBoundPool() {
        int cores = Runtime.getRuntime().availableProcessors();
        int maxThreads = cores * 2; // Higher for I/O-bound

        return Executors.newFixedThreadPool(maxThreads);
    }

    /**
     * Graceful shutdown with timeout
     */
    public static void shutdownGracefully(ExecutorService executor, Duration timeout) {
        executor.shutdown(); // Reject new tasks

        try {
            if (!executor.awaitTermination(timeout.toMillis(), TimeUnit.MILLISECONDS)) {
                executor.shutdownNow(); // Force shutdown
                if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                    System.err.println("Executor did not terminate");
                }
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }

    // Thread Pool Key Principles:
    // 1. Sizing: CPU-bound = cores, I/O-bound = cores * (1 + wait/compute ratio)
    // 2. Queue: Bounded queue prevents memory exhaustion
    // 3. Rejection policy: CallerRunsPolicy, AbortPolicy, DiscardPolicy
    // 4. Shutdown: Always shutdown executors to prevent thread leaks
    // 5. Monitoring: Track queue size, active threads, completed tasks
}
```

### 5. Resilience4j Retry Pattern
```java
// Pattern: Retry with exponential backoff using Resilience4j
import io.github.resilience4j.retry.*;
import io.github.resilience4j.retry.RetryConfig.*;
import java.time.Duration;
import java.util.function.Supplier;

public class ResiliencePatterns {
    /**
     * Execute operation with retry and exponential backoff.
     * Resilience4j is production-grade resilience library.
     */
    public static <T> T executeWithRetry(
            Supplier<T> operation,
            int maxRetries
    ) {
        RetryConfig config = RetryConfig.custom()
            .maxAttempts(maxRetries)
            .waitDuration(Duration.ofMillis(100))
            .intervalFunction(IntervalFunction.ofExponentialBackoff(
                Duration.ofMillis(100),
                2.0 // Multiplier: 100ms, 200ms, 400ms, 800ms...
            ))
            .retryExceptions(RuntimeException.class)
            .ignoreExceptions(IllegalArgumentException.class)
            .build();

        Retry retry = Retry.of("operationRetry", config);

        // Add event listeners for monitoring
        retry.getEventPublisher()
            .onRetry(event -> System.out.println("Retry attempt: " + event.getNumberOfRetryAttempts()))
            .onError(event -> System.err.println("All retries failed: " + event.getLastThrowable()));

        Supplier<T> decoratedSupplier = Retry.decorateSupplier(retry, operation);
        return decoratedSupplier.get();
    }

    // Resilience4j Key Principles:
    // 1. Circuit breaker: Prevent cascading failures
    // 2. Rate limiter: Control request rate to external services
    // 3. Bulkhead: Isolate resources to prevent one failure affecting others
    // 4. Time limiter: Timeout for operations
    // 5. Event monitoring: Track retries, failures, successes for observability
}
```
