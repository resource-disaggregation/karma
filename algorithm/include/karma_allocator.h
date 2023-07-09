#ifndef KARMA_ALLOCATOR_H
#define KARMA_ALLOCATOR_H

#include <vector>
#include <map>
#include <unordered_map>

namespace karma {

class karma_allocator {
 public:
  karma_allocator(uint32_t num_slices, float alpha, uint64_t init_credits = 999999999999ULL);

  virtual ~karma_allocator() = default;

  /**
   * @brief Add a user to the systems
   * @param user_id unique identifier for the user
   */
  void add_user(std::string user_id);

  /**
   * @brief Update the demand of a particular user
   * @param user_id unique identifier for the user
   * @param demand demand in slices
   */
  void update_demand(std::string user_id, uint32_t demand);
  
  /**
   * @brief Compute user allocations based on the current demands
   */
  void allocate();

  /**
   * @brief Query the current allocation for a particular user
   * @return Allocation in slices
   */
  uint32_t get_allocation(std::string user_id);

  /**
   * @brief Query the current number of credits for a particular user
   * @return Number of credits
   */
  uint64_t get_credits(std::string user_id);


private:

// Optimized karma algorithm
void karma_algorithm_fast(std::unordered_map<std::string, uint32_t> &demands);
void borrow_from_poorest_fast(std::unordered_map<std::string, uint32_t> &demands, std::vector<std::string>& donors, std::vector<std::string>& borrowers);
void give_to_richest_fast(std::unordered_map<std::string, uint32_t> &demands, std::vector<std::string>& donors, std::vector<std::string>& borrowers);

std::size_t total_blocks_;
uint32_t num_tenants_;
uint64_t init_credits_;

std::unordered_map<std::string, uint32_t> demands_;
std::unordered_map<std::string, uint64_t> credits_;
std::unordered_map<std::string, int32_t> rate_;
std::unordered_map<std::string, uint32_t> allocations_;

uint32_t public_blocks_;

};

}

#endif //KARMA_ALLOCATOR_H
