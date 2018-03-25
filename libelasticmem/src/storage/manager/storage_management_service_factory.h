#ifndef ELASTICMEM_KV_MANAGEMENT_RPC_SERVICE_FACTORY_H
#define ELASTICMEM_KV_MANAGEMENT_RPC_SERVICE_FACTORY_H

#include "storage_management_service.h"
#include "../block.h"
#include "../chain_module.h"

namespace elasticmem {
namespace storage {

class storage_management_service_factory : public storage_management_serviceIfFactory {
 public:
  explicit storage_management_service_factory(std::vector<std::shared_ptr<chain_module>> &blocks);
  storage_management_serviceIf *getHandler(const ::apache::thrift::TConnectionInfo &connInfo) override;
  void releaseHandler(storage_management_serviceIf *anIf) override;
 private:
  std::vector<std::shared_ptr<chain_module>> &blocks_;
};

}
}

#endif //ELASTICMEM_KV_MANAGEMENT_RPC_SERVICE_FACTORY_H
