#ifndef JIFFY_DBA_CLIENT_H
#define JIFFY_DBA_CLIENT_H

#include <cerrno>
#include "jiffy/directory/client/directory_client.h"
#include "jiffy/storage/client/replica_chain_client.h"
#include "jiffy/utils/client_cache.h"
#include "jiffy/storage/file/file_ops.h"
#include "jiffy/storage/client/data_structure_client.h"

namespace jiffy {
namespace storage {

// Direct block access client
class dba_client : public data_structure_client {
 public:
  
  dba_client(std::shared_ptr<directory::directory_interface> fs,
                    const std::string &path,
                    const directory::data_status &status,
                    int timeout_ms = 1000,
                    std::size_t block_size = 134217728);

  /**
   * @brief Destructor
   */
  virtual ~dba_client() = default;
  
  // Returns number of bytes read if successful (result appended to buf)
  // returns negative value on error:
  // -EINVAL: invalid arguments
  // -EACCES: block ownsership changed (stale sequence number)
  // -EPROTO: other errors 
  int read(const std::string &bid, std::string& buf, size_t offset, size_t size);

  // Returns number of bytes written if successful
  // returns negative value on error:
  // -EINVAL: invalid arguments
  // -EACCES: block ownsership changed (stale sequence number)
  // -EPROTO: other errors  
  int write(const std::string &bid, size_t offset, const std::string &data);

  void refresh() override;

  void handle_redirect(std::vector<std::string> &_return, const std::vector<std::string> &args) override;

 protected:

  std::shared_ptr<replica_chain_client> get_block_client(const std::string &bid);

  /* Map from block id -> replica chain client */
  std::map<std::string, std::shared_ptr<replica_chain_client>> blocks_;
  /* Block size */
  std::size_t block_size_;
};

}
}

#endif //JIFFY_DBA_CLIENT_H
