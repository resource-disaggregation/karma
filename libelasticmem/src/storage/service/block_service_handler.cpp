#include "block_service_handler.h"

namespace elasticmem {
namespace storage {

block_service_handler::block_service_handler(std::vector<std::shared_ptr<chain_module>> &blocks,
                                               std::vector<std::shared_ptr<subscription_map>> &sub_maps)
    : blocks_(blocks), sub_maps_(sub_maps) {}

void block_service_handler::run_command(std::vector<std::string> &_return,
                                        int64_t seq_no,
                                        const int32_t block_id,
                                        const int32_t cmd_id,
                                        const std::vector<std::string> &arguments) {
  try {
    auto blk = blocks_.at(static_cast<std::size_t>(block_id));
    blk->run_command_chain(_return, seq_no, cmd_id, arguments);
    sub_maps_.at(static_cast<std::size_t>(block_id))->notify(blk->op_name(cmd_id), arguments[0]); // FIXME
  } catch (std::exception& e) {
    throw make_exception(e);
  }
}

block_exception block_service_handler::make_exception(const std::exception &ex) {
  block_exception e;
  e.msg = ex.what();
  return e;
}


}
}