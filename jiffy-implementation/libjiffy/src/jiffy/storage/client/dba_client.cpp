#include "dba_client.h"
#include "jiffy/utils/logger.h"
#include "jiffy/utils/string_utils.h"
#include "jiffy/directory/directory_ops.h"
#include <algorithm>
#include <thread>
#include <utility>

namespace jiffy {
namespace storage {

using namespace jiffy::utils;

dba_client::dba_client(std::shared_ptr<directory::directory_interface> fs,
                         const std::string &path,
                         const directory::data_status &status,
                         int timeout_ms,
                         std::size_t block_size)
    : data_structure_client(std::move(fs), path, status, timeout_ms) {
  block_size_ = block_size;
}

std::shared_ptr<replica_chain_client> dba_client::get_block_client(const std::string &bid) {
  // if block client is not cached, create new one and add to cache
  if(blocks_.find(bid) == blocks_.end()) {
    std::vector<std::string> block_ids;
    block_ids.push_back(bid);
    directory::replica_chain chain(block_ids);
    blocks_[bid] = std::make_shared<replica_chain_client>(fs_, path_, chain, FILE_OPS, timeout_ms_);
  }

  return blocks_[bid];
}

int dba_client::read(const std::string &bid, std::string& buf, size_t offset, size_t size) {
  if(offset + size > block_size_) {
     return -EINVAL;
  }

  // Issue read via block client
  auto bclient = get_block_client(bid);
  std::vector<std::string>
        args{"read", std::to_string(offset), std::to_string(size)};
  bclient->send_command(args);

  // receive read response
  auto resp = bclient->recv_response();
  if(resp.front() == "!ok") {
    auto previous_size = buf.size();
    buf += resp.back();
    auto after_size = buf.size();
    return static_cast<int>(after_size - previous_size);
  } else if (resp.front() == "!stale_seq_no") {
    return -EACCES;
  } else {
    return -EPROTO;
  }
}

int dba_client::write(const std::string &bid, size_t offset, const std::string &data) {

  if(offset + data.size() > block_size_) {
     return -EINVAL;
  }

  // Issue write via block client
  auto bclient = get_block_client(bid);
  std::vector<std::string>
        args{"write", data, std::to_string(offset)};
  bclient->send_command(args);

  // wait for write response
  auto resp = bclient->recv_response();
  if(resp.front() == "!ok") {
    return static_cast<int>(data.size());
  } else if (resp.front() == "!stale_seq_no") {
    return -EACCES;
  } else {
    return -EPROTO;
  }
}

void dba_client::refresh() {
  // Do nothing
}

void dba_client::handle_redirect(std::vector<std::string> &, const std::vector<std::string> &) {
  // Do nothing
}

}
}
