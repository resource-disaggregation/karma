#ifndef ELASTICMEM_KV_SERVICE_SHARD_H
#define ELASTICMEM_KV_SERVICE_SHARD_H

#include <libcuckoo/cuckoohash_map.hh>

#include "../kv_management_service.h"
#include "../serializer/serde.h"
#include "../serializer/binary_serde.h"

namespace elasticmem {
namespace kv {

class noop_store : public persistent::persistent_service {
 public:
  void write(const std::string &, const std::string &) override {}
  void read(const std::string &, const std::string &) override {}
  void remove(const std::string &) override {}
};

class kv_block {
 public:
  typedef cuckoohash_map<key_type, value_type> block_type;
  typedef block_type::locked_table locked_block_type;

  explicit kv_block(std::shared_ptr<persistent::persistent_service> persistent = std::make_shared<noop_store>(),
                    std::string local_storage_prefix = "/tmp",
                    std::shared_ptr<serializer> ser = std::make_shared<binary_serializer>(),
                    std::shared_ptr<deserializer> deser = std::make_shared<binary_deserializer>());

  void put(const key_type &key, const value_type &value);

  value_type get(const key_type &key);

  void update(const key_type &key, const value_type &value);

  void remove(const key_type &key);

  std::size_t size() const;

  bool empty() const;

  void load(const std::string &remote_storage_prefix, const std::string &path);

  void flush(const std::string &remote_storage_prefix, const std::string &path);

  std::size_t storage_capacity();

  std::size_t storage_size();

  void clear();

 private:
  block_type block_;
  std::shared_ptr<persistent::persistent_service> persistent_;
  std::string local_storage_prefix_;
  std::shared_ptr<serializer> ser_;
  std::shared_ptr<deserializer> deser_;
};

}
}

#endif //ELASTICMEM_KV_SERVICE_SHARD_H
