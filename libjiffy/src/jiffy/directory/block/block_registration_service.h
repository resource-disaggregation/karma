/**
 * Autogenerated by Thrift Compiler (0.11.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
#ifndef block_registration_service_H
#define block_registration_service_H

#include <thrift/TDispatchProcessor.h>
#include <thrift/async/TConcurrentClientSyncInfo.h>
#include "block_registration_service_types.h"

namespace jiffy { namespace directory {

#ifdef _MSC_VER
  #pragma warning( push )
  #pragma warning (disable : 4250 ) //inheriting methods via dominance 
#endif

class block_registration_serviceIf {
 public:
  virtual ~block_registration_serviceIf() {}
  virtual void add_blocks(const std::vector<std::string> & block_names) = 0;
  virtual void remove_blocks(const std::vector<std::string> & block_names) = 0;
};

class block_registration_serviceIfFactory {
 public:
  typedef block_registration_serviceIf Handler;

  virtual ~block_registration_serviceIfFactory() {}

  virtual block_registration_serviceIf* getHandler(const ::apache::thrift::TConnectionInfo& connInfo) = 0;
  virtual void releaseHandler(block_registration_serviceIf* /* handler */) = 0;
};

class block_registration_serviceIfSingletonFactory : virtual public block_registration_serviceIfFactory {
 public:
  block_registration_serviceIfSingletonFactory(const ::apache::thrift::stdcxx::shared_ptr<block_registration_serviceIf>& iface) : iface_(iface) {}
  virtual ~block_registration_serviceIfSingletonFactory() {}

  virtual block_registration_serviceIf* getHandler(const ::apache::thrift::TConnectionInfo&) {
    return iface_.get();
  }
  virtual void releaseHandler(block_registration_serviceIf* /* handler */) {}

 protected:
  ::apache::thrift::stdcxx::shared_ptr<block_registration_serviceIf> iface_;
};

class block_registration_serviceNull : virtual public block_registration_serviceIf {
 public:
  virtual ~block_registration_serviceNull() {}
  void add_blocks(const std::vector<std::string> & /* block_names */) {
    return;
  }
  void remove_blocks(const std::vector<std::string> & /* block_names */) {
    return;
  }
};

typedef struct _block_registration_service_add_blocks_args__isset {
  _block_registration_service_add_blocks_args__isset() : block_names(false) {}
  bool block_names :1;
} _block_registration_service_add_blocks_args__isset;

class block_registration_service_add_blocks_args {
 public:

  block_registration_service_add_blocks_args(const block_registration_service_add_blocks_args&);
  block_registration_service_add_blocks_args& operator=(const block_registration_service_add_blocks_args&);
  block_registration_service_add_blocks_args() {
  }

  virtual ~block_registration_service_add_blocks_args() throw();
  std::vector<std::string>  block_names;

  _block_registration_service_add_blocks_args__isset __isset;

  void __set_block_names(const std::vector<std::string> & val);

  bool operator == (const block_registration_service_add_blocks_args & rhs) const
  {
    if (!(block_names == rhs.block_names))
      return false;
    return true;
  }
  bool operator != (const block_registration_service_add_blocks_args &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const block_registration_service_add_blocks_args & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

};


class block_registration_service_add_blocks_pargs {
 public:


  virtual ~block_registration_service_add_blocks_pargs() throw();
  const std::vector<std::string> * block_names;

  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

};

typedef struct _block_registration_service_add_blocks_result__isset {
  _block_registration_service_add_blocks_result__isset() : ex(false) {}
  bool ex :1;
} _block_registration_service_add_blocks_result__isset;

class block_registration_service_add_blocks_result {
 public:

  block_registration_service_add_blocks_result(const block_registration_service_add_blocks_result&);
  block_registration_service_add_blocks_result& operator=(const block_registration_service_add_blocks_result&);
  block_registration_service_add_blocks_result() {
  }

  virtual ~block_registration_service_add_blocks_result() throw();
  block_registration_service_exception ex;

  _block_registration_service_add_blocks_result__isset __isset;

  void __set_ex(const block_registration_service_exception& val);

  bool operator == (const block_registration_service_add_blocks_result & rhs) const
  {
    if (!(ex == rhs.ex))
      return false;
    return true;
  }
  bool operator != (const block_registration_service_add_blocks_result &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const block_registration_service_add_blocks_result & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

};

typedef struct _block_registration_service_add_blocks_presult__isset {
  _block_registration_service_add_blocks_presult__isset() : ex(false) {}
  bool ex :1;
} _block_registration_service_add_blocks_presult__isset;

class block_registration_service_add_blocks_presult {
 public:


  virtual ~block_registration_service_add_blocks_presult() throw();
  block_registration_service_exception ex;

  _block_registration_service_add_blocks_presult__isset __isset;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);

};

typedef struct _block_registration_service_remove_blocks_args__isset {
  _block_registration_service_remove_blocks_args__isset() : block_names(false) {}
  bool block_names :1;
} _block_registration_service_remove_blocks_args__isset;

class block_registration_service_remove_blocks_args {
 public:

  block_registration_service_remove_blocks_args(const block_registration_service_remove_blocks_args&);
  block_registration_service_remove_blocks_args& operator=(const block_registration_service_remove_blocks_args&);
  block_registration_service_remove_blocks_args() {
  }

  virtual ~block_registration_service_remove_blocks_args() throw();
  std::vector<std::string>  block_names;

  _block_registration_service_remove_blocks_args__isset __isset;

  void __set_block_names(const std::vector<std::string> & val);

  bool operator == (const block_registration_service_remove_blocks_args & rhs) const
  {
    if (!(block_names == rhs.block_names))
      return false;
    return true;
  }
  bool operator != (const block_registration_service_remove_blocks_args &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const block_registration_service_remove_blocks_args & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

};


class block_registration_service_remove_blocks_pargs {
 public:


  virtual ~block_registration_service_remove_blocks_pargs() throw();
  const std::vector<std::string> * block_names;

  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

};

typedef struct _block_registration_service_remove_blocks_result__isset {
  _block_registration_service_remove_blocks_result__isset() : ex(false) {}
  bool ex :1;
} _block_registration_service_remove_blocks_result__isset;

class block_registration_service_remove_blocks_result {
 public:

  block_registration_service_remove_blocks_result(const block_registration_service_remove_blocks_result&);
  block_registration_service_remove_blocks_result& operator=(const block_registration_service_remove_blocks_result&);
  block_registration_service_remove_blocks_result() {
  }

  virtual ~block_registration_service_remove_blocks_result() throw();
  block_registration_service_exception ex;

  _block_registration_service_remove_blocks_result__isset __isset;

  void __set_ex(const block_registration_service_exception& val);

  bool operator == (const block_registration_service_remove_blocks_result & rhs) const
  {
    if (!(ex == rhs.ex))
      return false;
    return true;
  }
  bool operator != (const block_registration_service_remove_blocks_result &rhs) const {
    return !(*this == rhs);
  }

  bool operator < (const block_registration_service_remove_blocks_result & ) const;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);
  template <class Protocol_>
  uint32_t write(Protocol_* oprot) const;

};

typedef struct _block_registration_service_remove_blocks_presult__isset {
  _block_registration_service_remove_blocks_presult__isset() : ex(false) {}
  bool ex :1;
} _block_registration_service_remove_blocks_presult__isset;

class block_registration_service_remove_blocks_presult {
 public:


  virtual ~block_registration_service_remove_blocks_presult() throw();
  block_registration_service_exception ex;

  _block_registration_service_remove_blocks_presult__isset __isset;

  template <class Protocol_>
  uint32_t read(Protocol_* iprot);

};

template <class Protocol_>
class block_registration_serviceClientT : virtual public block_registration_serviceIf {
 public:
  block_registration_serviceClientT(apache::thrift::stdcxx::shared_ptr< Protocol_> prot) {
    setProtocolT(prot);
  }
  block_registration_serviceClientT(apache::thrift::stdcxx::shared_ptr< Protocol_> iprot, apache::thrift::stdcxx::shared_ptr< Protocol_> oprot) {
    setProtocolT(iprot,oprot);
  }
 private:
  void setProtocolT(apache::thrift::stdcxx::shared_ptr< Protocol_> prot) {
  setProtocolT(prot,prot);
  }
  void setProtocolT(apache::thrift::stdcxx::shared_ptr< Protocol_> iprot, apache::thrift::stdcxx::shared_ptr< Protocol_> oprot) {
    piprot_=iprot;
    poprot_=oprot;
    iprot_ = iprot.get();
    oprot_ = oprot.get();
  }
 public:
  apache::thrift::stdcxx::shared_ptr< ::apache::thrift::protocol::TProtocol> getInputProtocol() {
    return this->piprot_;
  }
  apache::thrift::stdcxx::shared_ptr< ::apache::thrift::protocol::TProtocol> getOutputProtocol() {
    return this->poprot_;
  }
  void add_blocks(const std::vector<std::string> & block_names);
  void send_add_blocks(const std::vector<std::string> & block_names);
  void recv_add_blocks();
  void remove_blocks(const std::vector<std::string> & block_names);
  void send_remove_blocks(const std::vector<std::string> & block_names);
  void recv_remove_blocks();
 protected:
  apache::thrift::stdcxx::shared_ptr< Protocol_> piprot_;
  apache::thrift::stdcxx::shared_ptr< Protocol_> poprot_;
  Protocol_* iprot_;
  Protocol_* oprot_;
};

typedef block_registration_serviceClientT< ::apache::thrift::protocol::TProtocol> block_registration_serviceClient;

template <class Protocol_>
class block_registration_serviceProcessorT : public ::apache::thrift::TDispatchProcessorT<Protocol_> {
 protected:
  ::apache::thrift::stdcxx::shared_ptr<block_registration_serviceIf> iface_;
  virtual bool dispatchCall(::apache::thrift::protocol::TProtocol* iprot, ::apache::thrift::protocol::TProtocol* oprot, const std::string& fname, int32_t seqid, void* callContext);
  virtual bool dispatchCallTemplated(Protocol_* iprot, Protocol_* oprot, const std::string& fname, int32_t seqid, void* callContext);
 private:
  typedef  void (block_registration_serviceProcessorT::*ProcessFunction)(int32_t, ::apache::thrift::protocol::TProtocol*, ::apache::thrift::protocol::TProtocol*, void*);
  typedef void (block_registration_serviceProcessorT::*SpecializedProcessFunction)(int32_t, Protocol_*, Protocol_*, void*);
  struct ProcessFunctions {
    ProcessFunction generic;
    SpecializedProcessFunction specialized;
    ProcessFunctions(ProcessFunction g, SpecializedProcessFunction s) :
      generic(g),
      specialized(s) {}
    ProcessFunctions() : generic(NULL), specialized(NULL) {}
  };
  typedef std::map<std::string, ProcessFunctions> ProcessMap;
  ProcessMap processMap_;
  void process_add_blocks(int32_t seqid, ::apache::thrift::protocol::TProtocol* iprot, ::apache::thrift::protocol::TProtocol* oprot, void* callContext);
  void process_add_blocks(int32_t seqid, Protocol_* iprot, Protocol_* oprot, void* callContext);
  void process_remove_blocks(int32_t seqid, ::apache::thrift::protocol::TProtocol* iprot, ::apache::thrift::protocol::TProtocol* oprot, void* callContext);
  void process_remove_blocks(int32_t seqid, Protocol_* iprot, Protocol_* oprot, void* callContext);
 public:
  block_registration_serviceProcessorT(::apache::thrift::stdcxx::shared_ptr<block_registration_serviceIf> iface) :
    iface_(iface) {
    processMap_["add_blocks"] = ProcessFunctions(
      &block_registration_serviceProcessorT::process_add_blocks,
      &block_registration_serviceProcessorT::process_add_blocks);
    processMap_["remove_blocks"] = ProcessFunctions(
      &block_registration_serviceProcessorT::process_remove_blocks,
      &block_registration_serviceProcessorT::process_remove_blocks);
  }

  virtual ~block_registration_serviceProcessorT() {}
};

typedef block_registration_serviceProcessorT< ::apache::thrift::protocol::TDummyProtocol > block_registration_serviceProcessor;

template <class Protocol_>
class block_registration_serviceProcessorFactoryT : public ::apache::thrift::TProcessorFactory {
 public:
  block_registration_serviceProcessorFactoryT(const ::apache::thrift::stdcxx::shared_ptr< block_registration_serviceIfFactory >& handlerFactory) :
      handlerFactory_(handlerFactory) {}

  ::apache::thrift::stdcxx::shared_ptr< ::apache::thrift::TProcessor > getProcessor(const ::apache::thrift::TConnectionInfo& connInfo);

 protected:
  ::apache::thrift::stdcxx::shared_ptr< block_registration_serviceIfFactory > handlerFactory_;
};

typedef block_registration_serviceProcessorFactoryT< ::apache::thrift::protocol::TDummyProtocol > block_registration_serviceProcessorFactory;

class block_registration_serviceMultiface : virtual public block_registration_serviceIf {
 public:
  block_registration_serviceMultiface(std::vector<apache::thrift::stdcxx::shared_ptr<block_registration_serviceIf> >& ifaces) : ifaces_(ifaces) {
  }
  virtual ~block_registration_serviceMultiface() {}
 protected:
  std::vector<apache::thrift::stdcxx::shared_ptr<block_registration_serviceIf> > ifaces_;
  block_registration_serviceMultiface() {}
  void add(::apache::thrift::stdcxx::shared_ptr<block_registration_serviceIf> iface) {
    ifaces_.push_back(iface);
  }
 public:
  void add_blocks(const std::vector<std::string> & block_names) {
    size_t sz = ifaces_.size();
    size_t i = 0;
    for (; i < (sz - 1); ++i) {
      ifaces_[i]->add_blocks(block_names);
    }
    ifaces_[i]->add_blocks(block_names);
  }

  void remove_blocks(const std::vector<std::string> & block_names) {
    size_t sz = ifaces_.size();
    size_t i = 0;
    for (; i < (sz - 1); ++i) {
      ifaces_[i]->remove_blocks(block_names);
    }
    ifaces_[i]->remove_blocks(block_names);
  }

};

// The 'concurrent' client is a thread safe client that correctly handles
// out of order responses.  It is slower than the regular client, so should
// only be used when you need to share a connection among multiple threads
template <class Protocol_>
class block_registration_serviceConcurrentClientT : virtual public block_registration_serviceIf {
 public:
  block_registration_serviceConcurrentClientT(apache::thrift::stdcxx::shared_ptr< Protocol_> prot) {
    setProtocolT(prot);
  }
  block_registration_serviceConcurrentClientT(apache::thrift::stdcxx::shared_ptr< Protocol_> iprot, apache::thrift::stdcxx::shared_ptr< Protocol_> oprot) {
    setProtocolT(iprot,oprot);
  }
 private:
  void setProtocolT(apache::thrift::stdcxx::shared_ptr< Protocol_> prot) {
  setProtocolT(prot,prot);
  }
  void setProtocolT(apache::thrift::stdcxx::shared_ptr< Protocol_> iprot, apache::thrift::stdcxx::shared_ptr< Protocol_> oprot) {
    piprot_=iprot;
    poprot_=oprot;
    iprot_ = iprot.get();
    oprot_ = oprot.get();
  }
 public:
  apache::thrift::stdcxx::shared_ptr< ::apache::thrift::protocol::TProtocol> getInputProtocol() {
    return this->piprot_;
  }
  apache::thrift::stdcxx::shared_ptr< ::apache::thrift::protocol::TProtocol> getOutputProtocol() {
    return this->poprot_;
  }
  void add_blocks(const std::vector<std::string> & block_names);
  int32_t send_add_blocks(const std::vector<std::string> & block_names);
  void recv_add_blocks(const int32_t seqid);
  void remove_blocks(const std::vector<std::string> & block_names);
  int32_t send_remove_blocks(const std::vector<std::string> & block_names);
  void recv_remove_blocks(const int32_t seqid);
 protected:
  apache::thrift::stdcxx::shared_ptr< Protocol_> piprot_;
  apache::thrift::stdcxx::shared_ptr< Protocol_> poprot_;
  Protocol_* iprot_;
  Protocol_* oprot_;
  ::apache::thrift::async::TConcurrentClientSyncInfo sync_;
};

typedef block_registration_serviceConcurrentClientT< ::apache::thrift::protocol::TProtocol> block_registration_serviceConcurrentClient;

#ifdef _MSC_VER
  #pragma warning( pop )
#endif

}} // namespace

#include "block_registration_service.tcc"
#include "block_registration_service_types.tcc"

#endif
