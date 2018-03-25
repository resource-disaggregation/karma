#include "storage_management_service_handler.h"

namespace elasticmem {
namespace storage {

storage_management_service_handler::storage_management_service_handler(std::vector<std::shared_ptr<chain_module>> &blocks)
    : blocks_(blocks) {}

void storage_management_service_handler::setup_block(int32_t block_id,
                                                     const std::string &path,
                                                     int32_t role,
                                                     const std::string &next_block_name) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->path(path);
    blocks_.at(static_cast<std::size_t>(block_id))->role(static_cast<chain_role>(role));
    blocks_.at(static_cast<std::size_t>(block_id))->reset_next(next_block_name);
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::get_path(std::string &_return, const int32_t block_id) {
  try {
    _return = blocks_.at(static_cast<std::size_t>(block_id))->path();
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::flush(int32_t block_id,
                                               const std::string &persistent_store_prefix,
                                               const std::string &path) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->flush(persistent_store_prefix, path);
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::load(int32_t block_id,
                                              const std::string &persistent_store_prefix,
                                              const std::string &path) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->load(persistent_store_prefix, path);
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::reset(int32_t block_id) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->reset();
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

int64_t storage_management_service_handler::storage_capacity(int32_t block_id) {
  try {
    return static_cast<int64_t>(blocks_.at(static_cast<std::size_t>(block_id))->storage_capacity());
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

int64_t storage_management_service_handler::storage_size(int32_t block_id) {
  try {
    return static_cast<int64_t>(blocks_.at(static_cast<std::size_t>(block_id))->storage_size());
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

storage_management_exception storage_management_service_handler::make_exception(std::exception &e) {
  storage_management_exception ex;
  ex.msg = e.what();
  return ex;
}

}
}