#include "storage_management_service_handler.h"

namespace elasticmem {
namespace storage {

storage_management_service_handler::storage_management_service_handler(std::vector<std::shared_ptr<chain_module>> &blocks)
    : blocks_(blocks) {}

void storage_management_service_handler::setup_block(const int32_t block_id,
                                                     const std::string &path,
                                                     const int32_t slot_begin,
                                                     const int32_t slot_end,
                                                     const std::vector<std::string> &chain,
                                                     const int32_t role,
                                                     const std::string &next_block_name) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->path(path);
    blocks_.at(static_cast<std::size_t>(block_id))->slot_range(slot_begin, slot_end);
    blocks_.at(static_cast<std::size_t>(block_id))->chain(chain);
    blocks_.at(static_cast<std::size_t>(block_id))->role(static_cast<chain_role>(role));
    if (role == chain_role::tail && next_block_name != "nil") {
      // We're in recovery mode, forwarding requests
      blocks_.at(static_cast<std::size_t>(block_id))->reset_next(next_block_name);
    } else {
      blocks_.at(static_cast<std::size_t>(block_id))->reset_next_and_listen(next_block_name);
    }
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::set_exporting(const int32_t block_id,
                                                       const std::vector<std::string> &target_block,
                                                       const int32_t slot_begin,
                                                       const int32_t slot_end) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->state(block_state::exporting);
    blocks_.at(static_cast<std::size_t>(block_id))->export_target(target_block);
    blocks_.at(static_cast<std::size_t>(block_id))->export_slot_range(slot_begin, slot_end);
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}
void storage_management_service_handler::set_importing(const int32_t block_id,
                                                       const std::string &path,
                                                       const int32_t slot_begin,
                                                       const int32_t slot_end,
                                                       const std::vector<std::string> &chain,
                                                       const int32_t role,
                                                       const std::string &next_block_name) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->path(path);
    blocks_.at(static_cast<std::size_t>(block_id))->state(block_state::importing);
    blocks_.at(static_cast<std::size_t>(block_id))->slot_range(slot_begin, slot_end);
    blocks_.at(static_cast<std::size_t>(block_id))->chain(chain);
    blocks_.at(static_cast<std::size_t>(block_id))->role(static_cast<chain_role>(role));
    if (role == chain_role::tail && next_block_name != "nil") {
      // We're in recovery mode, forwarding requests
      blocks_.at(static_cast<std::size_t>(block_id))->reset_next(next_block_name);
    } else {
      blocks_.at(static_cast<std::size_t>(block_id))->reset_next_and_listen(next_block_name);
    }
  } catch (std::exception &e) {
    throw make_exception(e);
  }

}

void storage_management_service_handler::export_slots(const int32_t block_id) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->export_slots();
  } catch (std::exception& e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::set_regular(const int32_t block_id,
                                                     const int32_t slot_begin,
                                                     const int32_t slot_end) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->state(block_state::regular);
    blocks_.at(static_cast<std::size_t>(block_id))->slot_range(slot_begin, slot_end);
    blocks_.at(static_cast<std::size_t>(block_id))->export_target({});
    blocks_.at(static_cast<std::size_t>(block_id))->export_slot_range(0, -1);
  } catch (std::exception& e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::slot_range(rpc_slot_range &_return, const int32_t block_id) {
  auto range = blocks_.at(static_cast<std::size_t>(block_id))->slot_range();
  _return.slot_begin = range.first;
  _return.slot_end = range.second;
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

void storage_management_service_handler::resend_pending(const int32_t block_id) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->resend_pending();
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

void storage_management_service_handler::forward_all(const int32_t block_id) {
  try {
    blocks_.at(static_cast<std::size_t>(block_id))->forward_all();
  } catch (std::exception &e) {
    throw make_exception(e);
  }
}

storage_management_exception storage_management_service_handler::make_exception(std::exception &e) {
  storage_management_exception ex;
  ex.msg = e.what();
  return ex;
}

storage_management_exception storage_management_service_handler::make_exception(const std::string &msg) {
  storage_management_exception ex;
  ex.msg = msg;
  return ex;
}

}
}