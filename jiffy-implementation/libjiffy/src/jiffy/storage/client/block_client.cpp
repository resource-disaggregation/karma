#include <thrift/transport/TBufferTransports.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <iostream>

#include "block_client.h"

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;

namespace jiffy {
namespace storage {

block_client::~block_client() {
  if (transport_ != nullptr)
    disconnect();
}

int64_t block_client::get_client_id() {
  return client_->get_client_id();
}

void block_client::connect(const std::string &host, int port, int block_id, int timeout_ms, int block_seq_no) {
  block_id_ = block_id;
  block_seq_no_ = block_seq_no;
  auto sock = std::make_shared<TSocket>(host, port);
  if (timeout_ms > 0)
    sock->setRecvTimeout(timeout_ms);
  transport_ = std::shared_ptr<TTransport>(new TFramedTransport(sock));
  protocol_ = std::shared_ptr<TProtocol>(new TBinaryProtocol(transport_));
  client_ = std::make_shared<thrift_client>(protocol_);
  transport_->open();
}

block_client::command_response_reader block_client::get_command_response_reader(int64_t client_id) {
  client_->register_client_id(block_id_, client_id);
  return block_client::command_response_reader(protocol_);
}

void block_client::disconnect() {
  if (is_connected()) {
    transport_->close();
  }
  block_id_ = -1;
}

bool block_client::is_connected() const {
  if (transport_ == nullptr) return false;
  return transport_->isOpen();
}

void block_client::command_request(const sequence_id &seq, const std::vector<std::string> &args) {
  client_->command_request(seq, block_id_, inject_seq_no(args));
}

void block_client::send_run_command(const int32_t block_id, const std::vector<std::string> &arguments) {
  client_->send_run_command(block_id, inject_seq_no(arguments));
}

void block_client::recv_run_command(std::vector<std::string> &_return) {
  client_->recv_run_command(_return);
}

block_client::command_response_reader::command_response_reader(std::shared_ptr<apache::thrift::protocol::TProtocol> prot)
    : prot_(std::move(prot)) {
  iprot_ = prot_.get();
}

int64_t block_client::command_response_reader::recv_response(std::vector<std::string> &out) {
  using namespace ::apache::thrift::protocol;
  using namespace ::apache::thrift;
  int32_t rseqid = 0;
  std::string fname;
  TMessageType mtype;

  this->iprot_->readMessageBegin(fname, mtype, rseqid);
  if (mtype == T_EXCEPTION) {
    TApplicationException x;
    x.read(this->iprot_);
    this->iprot_->readMessageEnd();
    this->iprot_->getTransport()->readEnd();
    throw x;
  }
  block_response_service_response_args result;
  result.read(this->iprot_);
  this->iprot_->readMessageEnd();
  this->iprot_->getTransport()->readEnd();
  if (result.__isset.seq && result.__isset.result) {
    out = result.result;
    return result.seq.client_seq_no;
  }
  throw TApplicationException(TApplicationException::MISSING_RESULT, "Command failed: unknown result");
}

std::vector<std::string> block_client::inject_seq_no(const std::vector<std::string> &args) {
  std::vector<std::string> res;
  if(args.size() == 0) {
    return res;
  }
  res.push_back(args[0]);
  res.push_back("$block_seq_no$");
  res.push_back(std::to_string(block_seq_no_));
  for(int i = 1; i < args.size(); i++) {
    res.push_back(args[i]);
  }
  return res;
}

}
}
