#ifndef ELASTICMEM_KV_RPC_SERVICE_FACTORY_H
#define ELASTICMEM_KV_RPC_SERVICE_FACTORY_H

#include "block_service.h"
#include "../notification/subscription_map.h"
#include "../chain_module.h"

namespace elasticmem {
namespace storage {

class block_service_factory : public block_serviceIfFactory {
 public:
  explicit block_service_factory(std::vector<std::shared_ptr<chain_module>> &blocks,
                                  std::vector<std::shared_ptr<subscription_map>> &sub_maps);
  block_serviceIf *getHandler(const ::apache::thrift::TConnectionInfo &connInfo) override;
  void releaseHandler(block_serviceIf *anIf) override;
 private:
  std::vector<std::shared_ptr<chain_module>> &blocks_;
  std::vector<std::shared_ptr<subscription_map>> &sub_maps_;
};

}
}

#endif //ELASTICMEM_KV_RPC_SERVICE_FACTORY_H
