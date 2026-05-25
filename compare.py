from app import (
    ArrayStack,
    ArrayQueue,
    LinkedListStack,
    LinkedListQueue
)

import time
import matplotlib.pyplot as plt

# -------------------------
# Stack benchmark
# -------------------------

def benchmark_stack(stack_class, n=100000):
    stack = stack_class()

    # Push benchmark
    start_push = time.perf_counter()

    for i in range(n):
        stack.push(i)

    end_push = time.perf_counter()

    # Pop benchmark
    start_pop = time.perf_counter()

    while not stack.is_empty():
        stack.pop()

    end_pop = time.perf_counter()

    return {
        'push_time': end_push - start_push,
        'pop_time': end_pop - start_pop
    }


# -------------------------
# Queue benchmark
# -------------------------

def benchmark_queue(queue_class, n=100000):
    queue = queue_class()

    # Enqueue benchmark
    start_enqueue = time.perf_counter()

    for i in range(n):
        queue.enqueue(i)

    end_enqueue = time.perf_counter()

    # Dequeue benchmark
    start_dequeue = time.perf_counter()

    while not queue.is_empty():
        queue.dequeue()

    end_dequeue = time.perf_counter()

    return {
        'enqueue_time': end_enqueue - start_enqueue,
        'dequeue_time': end_dequeue - start_dequeue
    }


# -------------------------
# Display result
# -------------------------

def display_stack_result(name, result):
    print(f'{name}')
    print(f'Push time: {result["push_time"]:.6f} seconds')
    print(f'Pop time: {result["pop_time"]:.6f} seconds')
    print()


def display_queue_result(name, result):
    print(f'{name}')
    print(f'Enqueue time: {result["enqueue_time"]:.6f} seconds')
    print(f'Dequeue time: {result["dequeue_time"]:.6f} seconds')
    print()

def plot_queue_comparison(
    array_result,
    linked_result
):
    queue_names = [
        'Array Queue',
        'Linked List Queue'
    ]

    dequeue_times = [
        array_result['dequeue_time'],
        linked_result['dequeue_time']
    ]

    plt.bar(queue_names, dequeue_times)

    plt.ylabel('Time (seconds)')

    plt.title('Queue Dequeue Performance Comparison')

    plt.show()

# -------------------------
# Complexity table
# -------------------------

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


# -------------------------
# Main comparison
# -------------------------

def main():
    display_complexity()

    print('STACK COMPARISON')
    print('--------------------------------')

    array_stack_result = benchmark_stack(ArrayStack)
    linked_stack_result = benchmark_stack(LinkedListStack)

    display_stack_result('Array Stack', array_stack_result)
    display_stack_result('Linked List Stack', linked_stack_result)

    print('QUEUE COMPARISON')
    print('--------------------------------')

    array_queue_result = benchmark_queue(ArrayQueue)
    linked_queue_result = benchmark_queue(LinkedListQueue)

    display_queue_result('Array Queue', array_queue_result)
    display_queue_result('Linked List Queue', linked_queue_result)
    plot_queue_comparison(array_queue_result, linked_queue_result)

main()
