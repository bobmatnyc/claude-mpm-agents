---
name: python-async-patterns
description: 5 async patterns with full implementations for Python concurrent programming
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "5 production-ready async patterns: gather, worker pools, retry with backoff, TaskGroup, AsyncWorkerPool"
    when_to_use: "When implementing async/concurrent operations in Python"
    quick_start: "Choose pattern based on use case: gather for parallel ops, worker pool for rate limiting, retry for unreliable services"
context_limit: 700
tags:
  - python
  - async
  - asyncio
  - concurrency
  - worker-pool
  - retry
  - backoff
  - gather
  - task-group
requires_tools: []
---

# Async Programming Patterns

## Concurrent Task Execution

```python
# Pattern 1: Gather with timeout and error handling
async def process_concurrent_tasks(
    tasks: list[Coroutine[Any, Any, T]],
    timeout: float = 10.0
) -> list[T | Exception]:
    """Process tasks concurrently with timeout and exception handling."""
    try:
        async with asyncio.timeout(timeout):  # Python 3.11+
            # return_exceptions=True prevents one failure from cancelling others
            return await asyncio.gather(*tasks, return_exceptions=True)
    except asyncio.TimeoutError:
        logger.warning("Tasks timed out after %s seconds", timeout)
        raise
```

## Worker Pool with Concurrency Control

```python
# Pattern 2: Semaphore-based worker pool
async def worker_pool(
    tasks: list[Callable[[], Coroutine[Any, Any, T]]],
    max_workers: int = 10
) -> list[T]:
    """Execute tasks with bounded concurrency using semaphore."""
    semaphore = asyncio.Semaphore(max_workers)

    async def bounded_task(task: Callable) -> T:
        async with semaphore:
            return await task()

    return await asyncio.gather(*[bounded_task(t) for t in tasks])
```

## Retry with Exponential Backoff

```python
# Pattern 3: Resilient async operations with retries
async def retry_with_backoff(
    coro: Callable[[], Coroutine[Any, Any, T]],
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,)
) -> T:
    """Retry async operation with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await coro()
        except exceptions as e:
            if attempt == max_retries - 1:
                raise
            delay = backoff_factor ** attempt
            logger.warning("Attempt %d failed, retrying in %s seconds", attempt + 1, delay)
            await asyncio.sleep(delay)
```

## Task Cancellation and Cleanup

```python
# Pattern 4: Graceful task cancellation
async def cancelable_task_group(
    tasks: list[Coroutine[Any, Any, T]]
) -> list[T]:
    """Run tasks with automatic cancellation on first exception."""
    async with asyncio.TaskGroup() as tg:  # Python 3.11+
        results = [tg.create_task(task) for task in tasks]
    return [r.result() for r in results]
```

## Production-Ready AsyncWorkerPool

```python
# Pattern 5: Async Worker Pool with Retries and Exponential Backoff
import asyncio
from typing import Callable, Any, Optional
from dataclasses import dataclass
import time
import logging

logger = logging.getLogger(__name__)

@dataclass
class TaskResult:
    """Result of task execution with retry metadata."""
    success: bool
    result: Any = None
    error: Optional[Exception] = None
    attempts: int = 0
    total_time: float = 0.0

class AsyncWorkerPool:
    """Worker pool with configurable retry logic and exponential backoff.

    Features:
    - Fixed number of worker tasks
    - Task queue with asyncio.Queue
    - Retry logic with exponential backoff
    - Graceful shutdown with drain semantics
    - Per-task retry tracking

    Example:
        pool = AsyncWorkerPool(num_workers=5, max_retries=3)
        result = await pool.submit(my_async_task)
        await pool.shutdown()
    """

    def __init__(self, num_workers: int, max_retries: int):
        """Initialize worker pool.

        Args:
            num_workers: Number of concurrent worker tasks
            max_retries: Maximum retry attempts per task (0 = no retries)
        """
        self.num_workers = num_workers
        self.max_retries = max_retries
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.workers: list[asyncio.Task] = []
        self.shutdown_event = asyncio.Event()
        self._start_workers()

    def _start_workers(self) -> None:
        """Start worker tasks that process from queue."""
        for i in range(self.num_workers):
            worker = asyncio.create_task(self._worker(i))
            self.workers.append(worker)

    async def _worker(self, worker_id: int) -> None:
        """Worker coroutine that processes tasks from queue.

        Continues until shutdown_event is set AND queue is empty.
        """
        while not self.shutdown_event.is_set() or not self.task_queue.empty():
            try:
                # Wait for task with timeout to check shutdown periodically
                task_data = await asyncio.wait_for(
                    self.task_queue.get(),
                    timeout=0.1
                )

                # Process task with retries
                await self._execute_with_retry(task_data)
                self.task_queue.task_done()

            except asyncio.TimeoutError:
                # No task available, continue to check shutdown
                continue
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")

    async def _execute_with_retry(
        self,
        task_data: dict[str, Any]
    ) -> None:
        """Execute task with exponential backoff retry logic.

        Args:
            task_data: Dict with 'task' (callable) and 'future' (to set result)
        """
        task: Callable = task_data['task']
        future: asyncio.Future = task_data['future']

        last_error: Optional[Exception] = None
        start_time = time.time()

        for attempt in range(self.max_retries + 1):
            try:
                # Execute the task
                result = await task()

                # Success! Set result and return
                if not future.done():
                    future.set_result(TaskResult(
                        success=True,
                        result=result,
                        attempts=attempt + 1,
                        total_time=time.time() - start_time
                    ))
                return

            except Exception as e:
                last_error = e

                # If we've exhausted retries, fail
                if attempt >= self.max_retries:
                    break

                # Exponential backoff: 0.1s, 0.2s, 0.4s, 0.8s, ...
                backoff_time = 0.1 * (2 ** attempt)
                logger.warning(
                    f"Task failed (attempt {attempt + 1}/{self.max_retries + 1}), "
                    f"retrying in {backoff_time}s: {e}"
                )
                await asyncio.sleep(backoff_time)

        # All retries exhausted, set failure result
        if not future.done():
            future.set_result(TaskResult(
                success=False,
                error=last_error,
                attempts=self.max_retries + 1,
                total_time=time.time() - start_time
            ))

    async def submit(self, task: Callable) -> Any:
        """Submit task to worker pool and wait for result.

        Args:
            task: Async callable to execute

        Returns:
            TaskResult with execution metadata

        Raises:
            RuntimeError: If pool is shutting down
        """
        if self.shutdown_event.is_set():
            raise RuntimeError("Cannot submit to shutdown pool")

        # Create future to receive result
        future: asyncio.Future = asyncio.Future()

        # Add task to queue
        await self.task_queue.put({'task': task, 'future': future})

        # Wait for result
        return await future

    async def shutdown(self, timeout: Optional[float] = None) -> None:
        """Gracefully shutdown worker pool.

        Drains queue, then cancels workers after timeout.

        Args:
            timeout: Max time to wait for queue drain (None = wait forever)
        """
        # Signal shutdown
        self.shutdown_event.set()

        # Wait for queue to drain
        try:
            if timeout:
                await asyncio.wait_for(
                    self.task_queue.join(),
                    timeout=timeout
                )
            else:
                await self.task_queue.join()
        except asyncio.TimeoutError:
            logger.warning("Shutdown timeout, forcing worker cancellation")

        # Cancel all workers
        for worker in self.workers:
            worker.cancel()

        # Wait for workers to finish
        await asyncio.gather(*self.workers, return_exceptions=True)

# Usage Example:
async def example_usage():
    # Create pool with 5 workers, max 3 retries
    pool = AsyncWorkerPool(num_workers=5, max_retries=3)

    # Define task that might fail
    async def flaky_task():
        import random
        if random.random() < 0.5:
            raise ValueError("Random failure")
        return "success"

    # Submit task
    result = await pool.submit(flaky_task)

    if result.success:
        print(f"Task succeeded: {result.result} (attempts: {result.attempts})")
    else:
        print(f"Task failed after {result.attempts} attempts: {result.error}")

    # Graceful shutdown
    await pool.shutdown(timeout=5.0)

# Key Concepts:
# - Worker pool: Fixed workers processing from shared queue
# - Exponential backoff: 0.1 * (2 ** attempt) seconds
# - Graceful shutdown: Drain queue, then cancel workers
# - Future pattern: Submit returns future, worker sets result
# - TaskResult dataclass: Track attempts, time, success/failure
```

## When to Use Each Pattern

- **Gather with timeout**: Multiple independent operations (API calls, DB queries)
- **Worker pool (simple)**: Rate-limited operations (API with rate limits, DB connection pool)
- **Retry with backoff**: Unreliable external services (network calls, third-party APIs)
- **TaskGroup**: Related operations where failure of one should cancel others
- **AsyncWorkerPool (production)**: Production systems needing retry logic, graceful shutdown, task tracking
