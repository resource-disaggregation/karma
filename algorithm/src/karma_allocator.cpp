#include <algorithm>
#include <stdexcept>
#include "bheap.h"
#include "karma_allocator.h"


namespace karma {

karma_allocator::karma_allocator(uint32_t num_slices, float alpha, uint64_t init_credits) {
    total_blocks_ = num_slices;
    if(!(alpha >= 0.0 && alpha <= 1.0)) {
        throw std::invalid_argument("alpha value not between 0 and 1");
    }
    public_blocks_ = (uint32_t)(alpha*total_blocks_);
    init_credits_ = init_credits;
    num_tenants_ = 0;
}

void karma_allocator::add_user(std::string user_id) {
    demands_[user_id] = 0;
    allocations_[user_id] = 0;
    if(num_tenants_ == 0) {
        // Set initial credits
        credits_[user_id] = init_credits_;
    } else {
        // Initialize with average credits across users
        uint64_t sum_credits = 0;
        for(auto &it : credits_) {
            sum_credits += it.second;
        }
        credits_[user_id] = (sum_credits / num_tenants_);
    }
    rate_[user_id] = 0;
    num_tenants_ += 1;
}

void karma_allocator::update_demand(std::string user_id, uint32_t demand) {
    auto it = demands_.find(user_id);
    if(it == demands_.end()) {
        throw std::runtime_error("User does not exist");
    }
    it->second = demand;
}

uint32_t karma_allocator::get_allocation(std::string user_id) {
    auto it = allocations_.find(user_id);
    if(it == allocations_.end()) {
        throw std::runtime_error("User does not exist");
    }
    return it->second;
}

uint64_t karma_allocator::get_credits(std::string user_id) {
    auto it = credits_.find(user_id);
    if(it == credits_.end()) {
        throw std::runtime_error("User does not exist");
    }
    return it->second;
}

void karma_allocator::allocate() {
    auto fair_share = (total_blocks_ - public_blocks_) / num_tenants_;
    // Reset rates
    for(auto &jt : rate_) {
        jt.second = 0;
    }

    // Give every user free credits
    for(auto &jt : credits_) {
        jt.second += public_blocks_ / num_tenants_;
    }

    std::vector<std::string> donors, borrowers;
    uint32_t total_supply = 0;
    uint32_t total_demand = 0;
    for(auto &jt : demands_) {
        if(jt.second < fair_share) {
            donors.push_back(jt.first);
            total_supply += fair_share - jt.second;
        }
        else if(jt.second > fair_share) {
            borrowers.push_back(jt.first);
            total_demand += std::min(jt.second - fair_share, credits_[jt.first]);
        }
        // Allocate upto fair share
        allocations_[jt.first] = std::min(jt.second, (uint32_t) fair_share);
    }

    total_supply += public_blocks_;

    // Match supply to demand
    if(total_supply >= total_demand) {
        borrow_from_poorest_fast(demands_, donors, borrowers);
    }
    else if(total_supply < total_demand) 
    {
        give_to_richest_fast(demands_, donors, borrowers);
    }

    // Update credits based on computed rates
    for(auto &jt : rate_) {
        credits_[jt.first] += jt.second;
    }
}

namespace {
  struct karma_candidate {
    std::string id;
    int64_t c;
    uint32_t x;
  };

  bool poorer(const karma_candidate& a, const karma_candidate& b) 
  {
    return a.c < b.c;
  }

  bool richer(const karma_candidate& a, const karma_candidate& b) 
  {
    return a.c > b.c;
  }
}

// Note: this does NOT update credits_
void karma_allocator::borrow_from_poorest_fast(std::unordered_map<std::string, uint32_t> &demands, std::vector<std::string>& donors, std::vector<std::string>& borrowers) {

  auto fair_share = (total_blocks_ - public_blocks_) / num_tenants_;

  // Can satisfy demands of all borrowers
  uint32_t total_demand = 0;
  for(auto &b : borrowers) {
    auto to_borrow = std::min(credits_[b], demands[b] - fair_share);
    allocations_[b] += to_borrow;
    rate_[b] -= to_borrow;
    total_demand += to_borrow;
  }

  // Borrow from poorest donors and update their rates
  std::vector<karma_candidate> donor_list;
  for(auto &d : donors) {
    karma_candidate elem;
    elem.id = d;
    elem.c = credits_[d];
    elem.x = fair_share - demands[d];
    donor_list.push_back(elem);
  }
  // Give normal donors priority over shared slices
  if(public_blocks_ > 0)
  {
      donor_list.push_back({"$public$", (int64_t)(num_tenants_*init_credits_ + 777777), public_blocks_});
  }
  donor_list.push_back({"$dummy$", std::numeric_limits<int64_t>::max(), 0});

  // Sort donor_list by credits
  std::sort(donor_list.begin(), donor_list.end(), poorer);

  auto dem = total_demand;
  int64_t cur_c = -1;
  auto next_c = donor_list[0].c;
  // poorest active donor set (heap internally ordered by x)
  auto poorest_donors = BroadcastHeap();
  std::size_t idx = 0;

  while(dem > 0) {
    // Update poorest donors
    if(poorest_donors.size() == 0) {
      cur_c = next_c;
    //   assert(cur_c != std::numeric_limits<int64_t>::max());
    }
    while(donor_list[idx].c == cur_c) {
      poorest_donors.push(donor_list[idx].id, donor_list[idx].x);
      idx += 1;
    }
    next_c = donor_list[idx].c;

    // Perform c,x update
    if(dem < poorest_donors.size()) 
    {
      for(std::size_t i = 0; i < dem; i++) {
        bheap_item item = poorest_donors.pop();
        auto x = item.second - 1;
        dem -= 1;
        auto base_val = (item.first != "$public$")?(fair_share - demands[item.first]):(public_blocks_);
        rate_[item.first] += base_val - x;
      }
    } else {
      auto alpha = (int32_t) std::min({(int64_t)poorest_donors.min_val(), (int64_t)(dem/poorest_donors.size()), (int64_t)(next_c - cur_c)});
    //   assert(alpha > 0);
      poorest_donors.add_to_all(-1*alpha);
      cur_c += alpha;
      dem -= poorest_donors.size() * alpha;
    }

    // get rid of donors with x = 0
    while(poorest_donors.size() > 0 && poorest_donors.min_val() == 0) {
      bheap_item item = poorest_donors.pop();
      auto base_val = (item.first != "$public$")?(fair_share - demands[item.first]):(public_blocks_);
      rate_[item.first] += base_val;
    }

  }

  while(poorest_donors.size() > 0) {
    bheap_item item = poorest_donors.pop();
    auto base_val = (item.first != "$public$")?(fair_share - demands[item.first]):(public_blocks_);
    rate_[item.first] += base_val - item.second;
  }

}

// Note: this does NOT update credits_
void karma_allocator::give_to_richest_fast(std::unordered_map<std::string, uint32_t> &demands, std::vector<std::string>& donors, std::vector<std::string>& borrowers) {

  auto fair_share = (total_blocks_ - public_blocks_) / num_tenants_;

  // Can match all donations
  uint32_t total_supply = 0;
  for(auto &d : donors) {
    auto to_give = fair_share - demands[d];
    rate_[d] += to_give;
    total_supply += to_give;
  }
  if(public_blocks_ > 0) {
    rate_["$public$"] += public_blocks_;
    total_supply += public_blocks_; 
  }

  // # Give to richest borrowers and update their allocations/rate
  std::vector<karma_candidate> borrower_list;
  for(auto &b : borrowers) {
    karma_candidate elem;
    elem.id = b;
    elem.c = credits_[b];
    elem.x = std::min(credits_[b], demands[b] - fair_share);
    borrower_list.push_back(elem);
  }
  borrower_list.push_back({"$dummy$", -1, 0});

  std::sort(borrower_list.begin(), borrower_list.end(), richer);

  auto sup = total_supply;
  int64_t cur_c = std::numeric_limits<int64_t>::max();
  int64_t next_c = borrower_list[0].c;
  // richest active borrower set (heap internally ordered by x)
  auto richest_borrowers = BroadcastHeap();
  std::size_t idx = 0;

  while(sup > 0) {
    // Update richest borrowers
    if(richest_borrowers.size() == 0) {
      cur_c = next_c;
    //   assert(cur_c != std::numeric_limits<int64_t>::min());
    }
    while(borrower_list[idx].c == cur_c) {
      richest_borrowers.push(borrower_list[idx].id, borrower_list[idx].x);
      idx += 1;
    }
    next_c = borrower_list[idx].c;

    // perform c,x update
    if(sup < richest_borrowers.size()) {
      for(std::size_t i = 0; i < sup; i++) {
        bheap_item item = richest_borrowers.pop();
        auto x = item.second - 1;
        sup -= 1;
        auto delta = std::min(credits_[item.first], demands[item.first] - fair_share) - x;
        allocations_[item.first] += delta;
        rate_[item.first] -= delta;
      }
    } else {
      auto alpha = (int32_t) std::min((int64_t)(richest_borrowers.min_val()), (int64_t)(sup/richest_borrowers.size()));
    //   assert(alpha > 0);
      if(next_c != -1) {
        alpha = (int32_t) std::min((int64_t)alpha, (int64_t)(cur_c - next_c));
      }
      richest_borrowers.add_to_all(-1 * alpha);
      cur_c -= alpha;
      sup -= richest_borrowers.size() * alpha;
    }

    // Get rid of borrowers with x = 0
    while(richest_borrowers.size() > 0 && richest_borrowers.min_val() == 0) {
      bheap_item item = richest_borrowers.pop();
      auto delta = std::min(credits_[item.first], demands[item.first] - fair_share);
      allocations_[item.first] += delta;
      rate_[item.first] -= delta;
    }
  }

  while(richest_borrowers.size() > 0) {
    bheap_item item = richest_borrowers.pop();
    auto delta = std::min(credits_[item.first], demands[item.first] - fair_share) - item.second;
    allocations_[item.first] += delta;
    rate_[item.first] -= delta;
  }

}

}