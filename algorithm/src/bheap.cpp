#include "bheap.h"

namespace karma {

BroadcastHeap::BroadcastHeap() {
    base_val_ = 0;
}

void BroadcastHeap::push(const std::string &key, int32_t value) {
    h_.push(std::make_pair(key, value - base_val_));
}

bheap_item BroadcastHeap::pop() {
    bheap_item x = h_.top();
    h_.pop();
    return std::make_pair(x.first, x.second + base_val_);
}

int32_t BroadcastHeap::min_val() {
    return h_.top().second + base_val_;
}

void BroadcastHeap::add_to_all(int32_t delta) {
    base_val_ += delta;
}

std::size_t BroadcastHeap::size() {
    return h_.size();
}

}
