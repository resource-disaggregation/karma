#include <iostream>

#include "karma_allocator.h"

using namespace karma;

int main() {

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

    // Update demands of users
    allocator.update_demand("A", 0);
    allocator.update_demand("B", 3);
    allocator.update_demand("C", 0);
    // Compute allocations based on current demands
    allocator.allocate();
    // Output current allocations
    std::cout << "A: " << allocator.get_allocation("A") << " ";
    std::cout << "B: " << allocator.get_allocation("B") << " ";
    std::cout << "C: " << allocator.get_allocation("C") << std::endl;

    // Update demands of users
    allocator.update_demand("A", 2);
    allocator.update_demand("B", 2);
    allocator.update_demand("C", 5);
    // Compute allocations based on current demands
    allocator.allocate();
    // Output current allocations
    std::cout << "A: " << allocator.get_allocation("A") << " ";
    std::cout << "B: " << allocator.get_allocation("B") << " ";
    std::cout << "C: " << allocator.get_allocation("C") << std::endl;

    return 0;
}
