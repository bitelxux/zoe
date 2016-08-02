title Net wakeup

Net->Stats: update_stats()
Net->+Router: init()
Router->-Net: router
Net-->Router: start()
Net->+Puncher: init()
Puncher->-Net: puncher
Net-->Puncher: start()
Net->Net: renew_socket()
Net->Router: update_route(presenter)
Net->Router: keep_alive()

