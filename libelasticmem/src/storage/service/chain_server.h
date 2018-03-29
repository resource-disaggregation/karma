#ifndef ELASTICMEM_CHAIN_SERVER_H
#define ELASTICMEM_CHAIN_SERVER_H

#include <thrift/server/TThreadedServer.h>
#include "../chain_module.h"

namespace elasticmem {
namespace storage {

class chain_server {
 public:
  static std::shared_ptr<apache::thrift::server::TThreadedServer> create(std::vector<std::shared_ptr<chain_module>> &blocks,
                                                                         const std::string &address,
                                                                         int port);
};

}
}

#endif //ELASTICMEM_CHAIN_SERVER_H