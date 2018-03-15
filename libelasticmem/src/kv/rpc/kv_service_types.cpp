/**
 * Autogenerated by Thrift Compiler (0.11.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
#include "kv_service_types.h"

#include <algorithm>
#include <ostream>

#include <thrift/TToString.h>

namespace elasticmem {
namespace kv {

kv_rpc_exception::~kv_rpc_exception() throw() {
}

void kv_rpc_exception::__set_msg(const std::string &val) {
  this->msg = val;
}
std::ostream &operator<<(std::ostream &out, const kv_rpc_exception &obj) {
  obj.printTo(out);
  return out;
}

void swap(kv_rpc_exception &a, kv_rpc_exception &b) {
  using ::std::swap;
  swap(a.msg, b.msg);
  swap(a.__isset, b.__isset);
}

kv_rpc_exception::kv_rpc_exception(const kv_rpc_exception &other0) : TException() {
  msg = other0.msg;
  __isset = other0.__isset;
}
kv_rpc_exception &kv_rpc_exception::operator=(const kv_rpc_exception &other1) {
  msg = other1.msg;
  __isset = other1.__isset;
  return *this;
}
void kv_rpc_exception::printTo(std::ostream &out) const {
  using ::apache::thrift::to_string;
  out << "kv_rpc_exception(";
  out << "msg=" << to_string(msg);
  out << ")";
}

const char *kv_rpc_exception::what() const throw() {
  try {
    std::stringstream ss;
    ss << "TException - service has thrown: " << *this;
    this->thriftTExceptionMessageHolder_ = ss.str();
    return this->thriftTExceptionMessageHolder_.c_str();
  } catch (const std::exception &) {
    return "TException - service has thrown: kv_rpc_exception";
  }
}

kv_management_rpc_exception::~kv_management_rpc_exception() throw() {
}

void kv_management_rpc_exception::__set_msg(const std::string &val) {
  this->msg = val;
}
std::ostream &operator<<(std::ostream &out, const kv_management_rpc_exception &obj) {
  obj.printTo(out);
  return out;
}

void swap(kv_management_rpc_exception &a, kv_management_rpc_exception &b) {
  using ::std::swap;
  swap(a.msg, b.msg);
  swap(a.__isset, b.__isset);
}

kv_management_rpc_exception::kv_management_rpc_exception(const kv_management_rpc_exception &other2) : TException() {
  msg = other2.msg;
  __isset = other2.__isset;
}
kv_management_rpc_exception &kv_management_rpc_exception::operator=(const kv_management_rpc_exception &other3) {
  msg = other3.msg;
  __isset = other3.__isset;
  return *this;
}
void kv_management_rpc_exception::printTo(std::ostream &out) const {
  using ::apache::thrift::to_string;
  out << "kv_management_rpc_exception(";
  out << "msg=" << to_string(msg);
  out << ")";
}

const char *kv_management_rpc_exception::what() const throw() {
  try {
    std::stringstream ss;
    ss << "TException - service has thrown: " << *this;
    this->thriftTExceptionMessageHolder_ = ss.str();
    return this->thriftTExceptionMessageHolder_.c_str();
  } catch (const std::exception &) {
    return "TException - service has thrown: kv_management_rpc_exception";
  }
}

}
} // namespace
