from app import (
    ArrayStack,
    ArrayQueue,
    LinkedListStack,
    LinkedListQueue
)

import time
import matplotlib.pyplot as plt


# =========================================================
# STACK BENCHMARK
# =========================================================

def benchmark_stack(stack_class, n=100000):
    stack = stack_class()

    start_push = time.perf_counter()
    for i in range(n):
        stack.push(i)
    end_push = time.perf_counter()

    start_pop = time.perf_counter()
    while not stack.is_empty():
        stack.pop()
    end_pop = time.perf_counter()

    return {
        'push_time': end_push - start_push,
        'pop_time': end_pop - start_pop
    }


# =========================================================
# QUEUE BENCHMARK
# =========================================================

def benchmark_queue(queue_class, n=100000):
    queue = queue_class()

    start_enqueue = time.perf_counter()
    for i in range(n):
        queue.enqueue(i)
    end_enqueue = time.perf_counter()

    start_dequeue = time.perf_counter()
    while not queue.is_empty():
        queue.dequeue()
    end_dequeue = time.perf_counter()

    return {
        'enqueue_time': end_enqueue - start_enqueue,
        'dequeue_time': end_dequeue - start_dequeue
    }


# =========================================================
# AVERAGE (REPETITION TEST) - STACK
# =========================================================

def avg_stack_benchmark(func, cls, times=5):
    total_push = 0
    total_pop = 0

    for _ in range(times):
        result = func(cls)
        total_push += result['push_time']
        total_pop += result['pop_time']

    return {
        'push_time': total_push / times,
        'pop_time': total_pop / times
    }


# =========================================================
# AVERAGE (REPETITION TEST) - QUEUE
# =========================================================

def avg_queue_benchmark(func, cls, times=5):
    total_enqueue = 0
    total_dequeue = 0

    for _ in range(times):
        result = func(cls)
        total_enqueue += result['enqueue_time']
        total_dequeue += result['dequeue_time']

    return {
        'enqueue_time': total_enqueue / times,
        'dequeue_time': total_dequeue / times
    }


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_stack_result(name, result):
    print(f'{name}')
    print(f'Push time (avg): {result["push_time"]:.6f} seconds')
    print(f'Pop time (avg): {result["pop_time"]:.6f} seconds')
    print()


def display_queue_result(name, result):
    print(f'{name}')
    print(f'Enqueue time (avg): {result["enqueue_time"]:.6f} seconds')
    print(f'Dequeue time (avg): {result["dequeue_time"]:.6f} seconds')
    print()


# =========================================================
# VISUALIZATION
# =========================================================

def plot_queue_comparison(array_result, linked_result):
    queue_names = ['Array Queue', 'Linked List Queue']

    dequeue_times = [
        array_result['dequeue_time'],
        linked_result['dequeue_time']
    ]

    plt.bar(queue_names, dequeue_times)
    plt.ylabel('Time (seconds)')
    plt.title('Queue Dequeue Performance Comparison')
    plt.show()


# =========================================================
# COMPLEXITY TABLE
# =========================================================

def display_complexity():
    print('TIME COMPLEXITY')
    print('--------------------------------')

    print('Stack Operations')
    print('Push : Array O(1) | Linked List O(1)')
    print('Pop  : Array O(1) | Linked List O(1)')
    print()

    print('Queue Operations')
    print('Enqueue : Array O(1) | Linked List O(1)')
    print('Dequeue : Array O(n) | Linked List O(1)')
    print()


# =========================================================
# MAIN
# =========================================================

def main():
    display_complexity()

    print('STACK COMPARISON')
    print('--------------------------------')

    array_stack_result = avg_stack_benchmark(benchmark_stack, ArrayStack)
    linked_stack_result = avg_stack_benchmark(benchmark_stack, LinkedListStack)

    display_stack_result('Array Stack', array_stack_result)
    display_stack_result('Linked List Stack', linked_stack_result)

    print('QUEUE COMPARISON')
    print('--------------------------------')

    array_queue_result = avg_queue_benchmark(benchmark_queue, ArrayQueue)
    linked_queue_result = avg_queue_benchmark(benchmark_queue, LinkedListQueue)

    display_queue_result('Array Queue', array_queue_result)
    display_queue_result('Linked List Queue', linked_queue_result)

    plot_queue_comparison(array_queue_result, linked_queue_result)


if __name__ == "__main__":
    main()