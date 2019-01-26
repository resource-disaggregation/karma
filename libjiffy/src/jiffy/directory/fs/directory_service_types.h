/**
 * Autogenerated by Thrift Compiler (0.11.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
#ifndef directory_service_TYPES_H
#define directory_service_TYPES_H

#include <iosfwd>

#include <thrift/Thrift.h>
#include <thrift/TApplicationException.h>
#include <thrift/TBase.h>
#include <thrift/protocol/TProtocol.h>
#include <thrift/transport/TTransport.h>

#include <thrift/stdcxx.h>


namespace jiffy { namespace directory {

enum rpc_perm_options {
  rpc_replace = 0,
  rpc_add = 1,
  rpc_remove = 2
};

extern const std::map<int, const char*> _rpc_perm_options_VALUES_TO_NAMES;

std::ostream& operator<<(std::ostream& out, const rpc_perm_options val);

enum rpc_file_type {
  rpc_none = 0,
  rpc_regular = 1,
  rpc_directory = 2
};

extern const std::map<int, const char*> _rpc_file_type_VALUES_TO_NAMES;

std::ostream& operator<<(std::ostream& out, const rpc_file_type val);

enum rpc_storage_mode {
  rpc_in_memory = 0,
  rpc_in_memory_grace = 1,
  rpc_on_disk = 2
};

extern const std::map<int, const char*> _rpc_storage_mode_VALUES_TO_NAMES;

std::ostream& operator<<(std::ostream& out, const rpc_storage_mode val);

typedef int32_t rpc_perms;

class rpc_replica_chain;

class rpc_file_status;

class rpc_data_status;

class rpc_dir_entry;

class directory_service_exception;


class rpc_replica_chain {
 public:

  rpc_replica_chain(const rpc_replica_chain&);
  rpc_replica_chain& operator=(const rpc_replica_chain&);
  rpc_replica_chain() : name(), metadata(), storage_mode((rpc_storage_mode)0) {
  }

  virtual ~rpc_replica_chain() throw();
  std::vector<std::string>  block_names;
  std::string name;
  std::string metadata;
  rpc_storage_mode storage_mode;

  void __set_block_names(const std::vector<std::string> & val);

  void __set_name(const std::string& val);

  void __set_metadata(const std::string& val);

  void __set_storage_mode(const rpc_storage_mode val);

  bool operator == (const rpc_replica_chain & rhs) const
  {
    if (!(block_names == rhs.block_names))
      return false;
    if (!(name == rhs.name))
      return false;
    if (!(metadata == rhs.metadata))
      return false;
    if (!(storage_mode == rhs.storage_mode))
      return false;
    return true;
  }
  bool operator != (const rpc_replica_chain &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const rpc_replica_chain & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

  virtual void printTo(std::ostream& out) const;
};

void swap(rpc_replica_chain &a, rpc_replica_chain &b);

std::ostream& operator<<(std::ostream& out, const rpc_replica_chain& obj);


class rpc_file_status {
 public:

  rpc_file_status(const rpc_file_status&);
  rpc_file_status& operator=(const rpc_file_status&);
  rpc_file_status() : type((rpc_file_type)0), permissions(0), last_write_time(0) {
  }

  virtual ~rpc_file_status() throw();
  rpc_file_type type;
  rpc_perms permissions;
  int64_t last_write_time;

  void __set_type(const rpc_file_type val);

  void __set_permissions(const rpc_perms val);

  void __set_last_write_time(const int64_t val);

  bool operator == (const rpc_file_status & rhs) const
  {
    if (!(type == rhs.type))
      return false;
    if (!(permissions == rhs.permissions))
      return false;
    if (!(last_write_time == rhs.last_write_time))
      return false;
    return true;
  }
  bool operator != (const rpc_file_status &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const rpc_file_status & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

  virtual void printTo(std::ostream& out) const;
};

void swap(rpc_file_status &a, rpc_file_status &b);

std::ostream& operator<<(std::ostream& out, const rpc_file_status& obj);


class rpc_data_status {
 public:

  rpc_data_status(const rpc_data_status&);
  rpc_data_status& operator=(const rpc_data_status&);
  rpc_data_status() : type(), backing_path(), chain_length(0), flags(0) {
  }

  virtual ~rpc_data_status() throw();
  std::string type;
  std::string backing_path;
  int32_t chain_length;
  std::vector<rpc_replica_chain>  data_blocks;
  int32_t flags;
  std::map<std::string, std::string>  tags;

  void __set_type(const std::string& val);

  void __set_backing_path(const std::string& val);

  void __set_chain_length(const int32_t val);

  void __set_data_blocks(const std::vector<rpc_replica_chain> & val);

  void __set_flags(const int32_t val);

  void __set_tags(const std::map<std::string, std::string> & val);

  bool operator == (const rpc_data_status & rhs) const
  {
    if (!(type == rhs.type))
      return false;
    if (!(backing_path == rhs.backing_path))
      return false;
    if (!(chain_length == rhs.chain_length))
      return false;
    if (!(data_blocks == rhs.data_blocks))
      return false;
    if (!(flags == rhs.flags))
      return false;
    if (!(tags == rhs.tags))
      return false;
    return true;
  }
  bool operator != (const rpc_data_status &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const rpc_data_status & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

  virtual void printTo(std::ostream& out) const;
};

void swap(rpc_data_status &a, rpc_data_status &b);

std::ostream& operator<<(std::ostream& out, const rpc_data_status& obj);


class rpc_dir_entry {
 public:

  rpc_dir_entry(const rpc_dir_entry&);
  rpc_dir_entry& operator=(const rpc_dir_entry&);
  rpc_dir_entry() : name() {
  }

  virtual ~rpc_dir_entry() throw();
  std::string name;
  rpc_file_status status;

  void __set_name(const std::string& val);

  void __set_status(const rpc_file_status& val);

  bool operator == (const rpc_dir_entry & rhs) const
  {
    if (!(name == rhs.name))
      return false;
    if (!(status == rhs.status))
      return false;
    return true;
  }
  bool operator != (const rpc_dir_entry &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const rpc_dir_entry & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

  virtual void printTo(std::ostream& out) const;
};

void swap(rpc_dir_entry &a, rpc_dir_entry &b);

std::ostream& operator<<(std::ostream& out, const rpc_dir_entry& obj);


class directory_service_exception : public ::apache::thrift::TException {
 public:

  directory_service_exception(const directory_service_exception&);
  directory_service_exception& operator=(const directory_service_exception&);
  directory_service_exception() : msg() {
  }

  virtual ~directory_service_exception() throw();
  std::string msg;

  void __set_msg(const std::string& val);

  bool operator == (const directory_service_exception & rhs) const
  {
    if (!(msg == rhs.msg))
      return false;
    return true;
  }
  bool operator != (const directory_service_exception &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const directory_service_exception & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

  virtual void printTo(std::ostream& out) const;
  mutable std::string thriftTExceptionMessageHolder_;
  const char* what() const throw();
};

void swap(directory_service_exception &a, directory_service_exception &b);

std::ostream& operator<<(std::ostream& out, const directory_service_exception& obj);

}} // namespace

#include "directory_service_types.tcc"

#endif
