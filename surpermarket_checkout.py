import threading
import time
from queue import Queue

class QueueManagementSystem:
    def __init__(self, N):
        self.queue = Queue()  # Use thread-safe Queue for managing customers
        self.counters = [False] * N  # N is the number of self-checkout counters, False indicates an available counter
        self.locks = [threading.Lock() for _ in range(N)]  # Locks for each counter to manage concurrency

    # Function to add a customer to the queue
    def add_customer_to_queue(self, customer):
        self.queue.put(customer)
        self.assign_counter_if_available()

    # Function to assign a counter to a customer if available
    def assign_counter_if_available(self):
        if not self.queue.empty():
            for i in range(len(self.counters)):
                if not self.counters[i]:  # Check for an available counter
                    with self.locks[i]:  # Ensure thread-safe access to counters
                        if not self.counters[i]:  # Double-check counter availability
                            customer = self.queue.get()  # Remove the first customer from the queue
                            self.counters[i] = True  # Mark the counter as busy
                            threading.Thread(target=self.start_checkout, args=(i, customer)).start()
                            break

    # Function to start checkout process (this would be a placeholder for actual checkout logic)
    def start_checkout(self, counter_id, customer):
        # Simulate the checkout process with a sleep (replace with actual checkout logic)
        print(f"Checkout started for {customer} at counter {counter_id}")
        time.sleep(2)  # Simulate time taken for checkout
        self.checkout_complete(counter_id)

    # Function to mark checkout complete
    def checkout_complete(self, counter_id):
        with self.locks[counter_id]:  # Ensure thread-safe access to counters
            self.counters[counter_id] = False  # Mark the counter as available
        print(f"Checkout completed at counter {counter_id}")
        self.assign_counter_if_available()  # Assign the next customer in the queue if any

    # Function to handle customers leaving the queue (if they decide to leave before checkout)
    def remove_customer_from_queue(self, customer):
        with threading.Lock():  # Ensure thread-safe access to queue
            temp_queue = Queue()
            removed = False
            while not self.queue.empty():
                current_customer = self.queue.get()
                if current_customer != customer:
                    temp_queue.put(current_customer)
                else:
                    removed = True
            self.queue = temp_queue
            if removed:
                print(f"{customer} has left the queue")

# Example Usage
queue_management = QueueManagementSystem(3)

# Add customers to the queue
queue_management.add_customer_to_queue("Customer 1")
queue_management.add_customer_to_queue("Customer 2")
queue_management.add_customer_to_queue("Customer 3")

# Simulate checkout complete for counter 0
queue_management.checkout_complete(1)

# Add another customer
queue_management.add_customer_to_queue("Customer 4")

# Customer 2 leaves the queue before being assigned a counter
queue_management.remove_customer_from_queue("Customer 2")
