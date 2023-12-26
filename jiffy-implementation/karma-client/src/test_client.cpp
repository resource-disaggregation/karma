#include <vector>
#include <iostream>
#include <boost/program_options.hpp>
#include <jiffy/client/jiffy_client.h>
#include <jiffy/utils/logger.h>
#include <jiffy/utils/signal_handling.h>
#include <jiffy/utils/time_utils.h>

using namespace ::jiffy::client;
using namespace ::jiffy::directory;
using namespace ::jiffy::storage;
using namespace ::jiffy::utils;

using namespace ::apache::thrift;

int main() {
    std::string dir_host = "127.0.0.1";
    int dir_port = 9090;
    int lease_port = 9091;
    jiffy_client client(dir_host, dir_port, lease_port);

    auto blk_client = client.create_dba_client(128*1024*1024);
    std::string bid = "127.0.0.1:9095:9093:0:0";
    std::string data;
    int ret = blk_client->write(bid, 0, "hello world");
    if(ret != 11) {
        std::cout << "block write error. ret " << ret << std::endl;
        return -1;
    }
    ret = blk_client->read(bid, data, 0, 11);
    if(ret != 11) {
        std::cout << "block read error. ret " << ret << std::endl;
        return -1;
    }

    std::cout << "block read. data =  " << data << std::endl; 

    std::string bid1 = "127.0.0.1:9095:9093:0:1";
    ret = blk_client->write(bid1, 0, "hello world");
    if(ret != 11) {
        std::cout << "block write error. ret " << ret << std::endl;
        return -1;
    }

    std::cout << "trying read with stale sequence number" << std::endl;
    data = "";
    ret = blk_client->read(bid, data, 0, 11);
    if(ret != -EACCES) {
        std::cout << "block read did not return correct error. ret " << ret << std::endl;
        return -1;
    }

    std::cout << "trying read with correct sequence number" << std::endl;
    data = "";
    ret = blk_client->read(bid1, data, 0, 11);
    if(ret != 11) {
        std::cout << "block read error. ret " << ret << std::endl;
        return -1;
    }

    std::cout << "block read. data =  " << data << std::endl; 
    return 0;
}