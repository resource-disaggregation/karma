#include <thrift/transport/TTransportException.h>
#include "replica_chain_client.h"
#include "jiffy/utils/string_utils.h"
#include "jiffy/utils/logger.h"
#include "jiffy/storage/command.h"
#include "jiffy/storage/manager/detail/block_id_parser.h"

namespace jiffy {
namespace storage {

using namespace utils;

replica_chain_client::replica_chain_client(std::shared_ptr<directory::directory_interface> fs,
                                           const std::string &path,
                                           const directory::replica_chain &chain,
                                           const command_map &OPS,
                                           int timeout_ms) : fs_(fs), path_(path), in_flight_(false), OPS_(OPS) {
  seq_.client_id = -1;
  seq_.client_seq_no = 0;
  accessor_ = false;
  send_run_command_exception_ = false;
  connect(chain, timeout_ms);
  for (auto &op: OPS) {
    cmd_client_[op.first] = op.second.is_accessor() ? &tail_ : &head_;
  }
}

replica_chain_client::~replica_chain_client() {
  disconnect();
}

void replica_chain_client::disconnect() {
  head_.disconnect();
  tail_.disconnect();
}

const directory::replica_chain &replica_chain_client::chain() const {
  return chain_;
}

void replica_chain_client::connect(const directory::replica_chain &chain, int timeout_ms) {
  chain_ = chain;
  timeout_ms_ = timeout_ms;
  auto h = block_id_parser::parse(chain_.block_ids.front());
  head_.connect(h.host, h.service_port, h.id, timeout_ms, h.block_seq_no);
  seq_.client_id = head_.get_client_id();
  if (chain_.block_ids.size() == 1) {
    tail_ = head_;
  } else {
    auto t = block_id_parser::parse(chain_.block_ids.back());
    tail_.connect(t.host, t.service_port, t.id, timeout_ms, h.block_seq_no);
  }
  response_reader_ = tail_.get_command_response_reader(seq_.client_id);
  in_flight_ = false;
}

void replica_chain_client::send_command(const std::vector<std::string> &args) {
  if (in_flight_) {
    throw std::length_error("Cannot have more than one request in-flight");
  }
  if (OPS_[args[0]].is_accessor()) {
    try {
      accessor_ = true;
      // cmd_client_.at(args.front())->send_run_command(std::stoi(string_utils::split(chain_.tail(), ':').back()), args);
      cmd_client_.at(args.front())->send_run_command(args);
    } catch (std::exception &e) {
      send_run_command_exception_ = true;
    }
  } else {
    cmd_client_.at(args.front())->command_request(seq_, args);
  }
  in_flight_ = true;
}

std::vector<std::string> replica_chain_client::recv_response() {
  std::vector<std::string> ret;
  int64_t rseq;
  if (accessor_) {
    if (send_run_command_exception_) {
      ret.emplace_back("!block_moved");
    } else {
      try {
        tail_.recv_run_command(ret);
      } catch (std::exception &e) {
        if (!send_run_command_exception_) {
          ret.emplace_back("!block_moved");
        }
      }
    }
    send_run_command_exception_ = false;
  } else {
    rseq = response_reader_.recv_response(ret);
    if (rseq != seq_.client_seq_no) {
      throw std::logic_error(
          "SEQ: Expected=" + std::to_string(seq_.client_seq_no) + " Received=" + std::to_string(rseq));
    }
  }
  seq_.client_seq_no++;
  in_flight_ = false;
  accessor_ = false;
  return ret;
}

std::vector<std::string> replica_chain_client::run_command(const std::vector<std::string> &args) {
  std::vector<std::string> response;
  bool retry = false;
  while (response.empty()) {
    try {
      send_command(args);
      response = recv_response();
      if (retry && response[0] == "!duplicate_key") { // TODO: This is hash table specific logic
        response[0] = "!ok";
      }
    } catch (apache::thrift::transport::TTransportException &e) {
      LOG(log_level::info) << "Error in connection to chain: " << e.what();
      LOG(log_level::info) << args.front() << " " << chain_.name;
      for (const auto &x : chain_.block_ids)
        LOG(log_level::info) << x;
      connect(fs_->resolve_failures(path_, chain_), timeout_ms_);
      retry = true;
    } catch (std::logic_error &e) { // TODO: This is very iffy, we need to fix this
      response.clear();
      response.emplace_back("!block_moved");
      break;
    }
  }
  return response;
}

std::vector<std::string> replica_chain_client::run_command_redirected(const std::vector<std::string> &args) {
  auto args_copy = args;
  if (args_copy.back() != "!redirected")
    args_copy.emplace_back("!redirected");
  send_command(args_copy);
  return recv_response();
}

void replica_chain_client::set_chain_name_metadata(std::string &name, std::string &metadata) {
  chain_.name = name;
  chain_.metadata = metadata;
}

bool replica_chain_client::is_connected() const {
  return head_.is_connected() && tail_.is_connected();
}

}
}
