#include <catch.hpp>

#include <thrift/transport/TTransportException.h>
#include <thread>
#include "../src/directory/lease/directory_lease_client.h"
#include "../src/directory/lease/directory_lease_server.h"
#include "../src/directory/block/random_block_allocator.h"
#include "test_utils.h"

using namespace ::elasticmem::storage;
using namespace ::elasticmem::directory;
using namespace ::apache::thrift::transport;

#define NUM_BLOCKS 1
#define HOST "127.0.0.1"
#define PORT 9090

TEST_CASE("update_lease_test", "[update_lease]") {
  using namespace std::chrono_literals;

  auto alloc = std::make_shared<dummy_block_allocator>(4);
  auto sm = std::make_shared<dummy_storage_manager>();
  auto t = std::make_shared<directory_tree>(alloc, sm);
  auto server = directory_lease_server::create(t, HOST, PORT);
  std::thread serve_thread([&server] { server->serve(); });
  test_utils::wait_till_server_ready(HOST, PORT);

  directory_lease_client client(HOST, PORT);

  t->create_file("/sandbox/a/b/c/file.txt", "/tmp");
  t->create_file("/sandbox/a/b/file.txt", "/tmp");
  t->create_file("/sandbox/a/file.txt", "/tmp");

  rpc_lease_update update;
  update.to_renew = {"/sandbox/a/b/c/file.txt"};
  update.to_flush = {"/sandbox/a/b/file.txt"};
  update.to_remove = {"/sandbox/a/file.txt"};
  rpc_lease_ack ack;
  REQUIRE_NOTHROW(ack = client.update_leases(update));
  REQUIRE(ack.renewed == 1);
  REQUIRE(ack.flushed == 1);
  REQUIRE(ack.removed == 1);
  REQUIRE(t->exists("/sandbox/a/b/c/file.txt"));
  REQUIRE(t->mode("/sandbox/a/b/c/file.txt") == storage_mode::in_memory);
  REQUIRE(t->exists("/sandbox/a/b/file.txt"));
  REQUIRE(t->mode("/sandbox/a/b/file.txt") == storage_mode::on_disk);
  REQUIRE(!t->exists("/sandbox/a/file.txt"));
  REQUIRE(sm->COMMANDS.size() == 2);
  REQUIRE(sm->COMMANDS[0] == "flush:1:/tmp:/sandbox/a/b/file.txt");
  REQUIRE(sm->COMMANDS[1] == "reset:2");

  server->stop();
  if (serve_thread.joinable()) {
    serve_thread.join();
  }
}