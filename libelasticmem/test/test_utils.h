#ifndef ELASTICMEM_TEST_UTILS_H
#define ELASTICMEM_TEST_UTILS_H

#include <string>
#include <vector>
#include <iostream>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/transport/TSocket.h>
#include "../src/storage/storage_management_ops.h"
#include "../src/directory/block/block_allocator.h"
#include "../src/storage/kv/kv_block.h"
#include "../src/storage/notification/subscription_map.h"

class dummy_storage_manager : public elasticmem::storage::storage_management_ops {
 public:
  dummy_storage_manager() = default;

  void setup_block(const std::string &block_name,
                   const std::string &path,
                   int32_t role,
                   const std::string &next_block_name) override {
    COMMANDS.push_back("setup_block:" + block_name + ":" + path + ":" + std::to_string(role) + ":" + next_block_name);
  }

  std::string path(const std::string &block_name) override {
    COMMANDS.push_back("get_path:" + block_name);
    return "";
  }

  void load(const std::string &block_name,
            const std::string &persistent_path_prefix,
            const std::string &path) override {
    COMMANDS.push_back("load:" + block_name + ":" + persistent_path_prefix + ":" + path);
  }

  void flush(const std::string &block_name,
             const std::string &persistent_path_prefix,
             const std::string &path) override {
    COMMANDS.push_back("flush:" + block_name + ":" + persistent_path_prefix + ":" + path);
  }

  void reset(const std::string &block_name) override {
    COMMANDS.push_back("reset:" + block_name);
  }

  size_t storage_capacity(const std::string &block_name) override {
    COMMANDS.push_back("storage_capacity:" + block_name);
    return 0;
  }

  size_t storage_size(const std::string &block_name) override {
    COMMANDS.push_back("storage_size:" + block_name);
    return 0;
  }

  std::vector<std::string> COMMANDS{};
};

class dummy_block_allocator : public elasticmem::directory::block_allocator {
 public:
  explicit dummy_block_allocator(std::size_t num_blocks) : num_free_(num_blocks) {}

  std::string allocate(const std::string &) override {
    if (num_free_ == 0) {
      throw std::out_of_range("Cannot allocate since nothing is free");
    }
    std::string ret = std::to_string(num_alloc_);
    ++num_alloc_;
    --num_free_;
    return ret;
  }

  void free(const std::string &) override {
    if (num_alloc_ == 0) {
      throw std::out_of_range("Cannot free since nothing is allocated");
    }
    ++num_free_;
    --num_alloc_;
  }

  void add_blocks(const std::vector<std::string> &blocks) override {
    num_free_ += blocks.size();
  }

  void remove_blocks(const std::vector<std::string> &blocks) override {
    if (num_free_ < blocks.size()) {
      throw std::out_of_range("Cannot remove: not enough blocks");
    }
    num_free_ -= blocks.size();
  }

  size_t num_free_blocks() override {
    return num_free_;
  }

  size_t num_allocated_blocks() override {
    return num_alloc_;
  }

  size_t num_total_blocks() override {
    return num_alloc_ + num_free_;
  }

 private:
  std::size_t num_alloc_{};
  std::size_t num_free_{};
};

class test_utils {
 public:
  static void wait_till_server_ready(const std::string &host, int port) {
    bool check = true;
    while (check) {
      try {
        auto transport =
            std::shared_ptr<apache::thrift::transport::TTransport>(new apache::thrift::transport::TBufferedTransport(
                std::make_shared<apache::thrift::transport::TSocket>(host, port)));
        transport->open();
        transport->close();
        check = false;
      } catch (apache::thrift::transport::TTransportException &e) {
        usleep(100000);
      }
    }
  }

  static std::vector<std::shared_ptr<elasticmem::storage::chain_module>> init_kv_blocks(size_t num_blocks,
                                                                                        int32_t service_port,
                                                                                        int32_t management_port,
                                                                                        int32_t notification_port) {
    std::vector<std::shared_ptr<elasticmem::storage::chain_module>> blks;
    blks.resize(num_blocks);
    for (size_t i = 0; i < num_blocks; ++i) {
      std::string block_name = elasticmem::storage::block_name_parser::make("127.0.0.1", service_port, management_port,
                                                                            notification_port, static_cast<int32_t>(i));
      blks[i] = std::make_shared<elasticmem::storage::kv_block>(block_name);
    }
    return blks;
  }

  static std::vector<std::shared_ptr<elasticmem::storage::subscription_map>> init_submaps(size_t num_blocks) {
    std::vector<std::shared_ptr<elasticmem::storage::subscription_map>> sub_maps;
    sub_maps.resize(num_blocks);
    for (auto &sub_map : sub_maps) {
      sub_map = std::make_shared<elasticmem::storage::subscription_map>();
    }
    return sub_maps;
  }
};

#endif //ELASTICMEM_TEST_UTILS_H
