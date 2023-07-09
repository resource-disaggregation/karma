# Karma Algorithm Module

This directory contains an implementation of the Karma algorithm as a C++ library for easy integration with applications. The library provides an allocator module with a simple and general interface that takes user demands as input and computes the corresponding allocations. The module internally maintains the necessary state and data structures and executes an optimized implementation of the Karma algorithm which computes resource allocations in a batched fashion.

## Building

To build the library make sure you have cmake version 3.12 or greater, and run the following

```
mkdir build
cd build
cmake ..
make
```

## Usage

To use the allocator module, simply include `include/karma_allocator.h` in your source files and link `libkarma` (geenrated in `build/`) to your executable. The following is a code snippet that initializes an instance of the allocator and invokes its APIs (for full example, see `example/`):

```cpp
// Initialize Karma allocator with 6 slices and alpha=0.5
karma_allocator allocator(6, 0.5);
// Add 3 users
allocator.add_user("A");
allocator.add_user("B");
allocator.add_user("C");

// Update demands of users
allocator.update_demand("A", 4);
allocator.update_demand("B", 1);
allocator.update_demand("C", 1);
// Compute allocations based on current demands
allocator.allocate();
// Output current allocations
std::cout << "A: " << allocator.get_allocation("A") << " ";
std::cout << "B: " << allocator.get_allocation("B") << " ";
std::cout << "C: " << allocator.get_allocation("C") << std::endl;
```

