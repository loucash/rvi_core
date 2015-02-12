#!/usr/bin/python

#
# Copyright (C) 2015, Jaguar Land Rover
#
# This program is licensed under the terms and conditions of the
# Mozilla Public License, version 2.0.  The full text of the 
# Mozilla Public License is at https://www.mozilla.org/MPL/2.0/
#
#
# Register a service specified by command line with an RVI node.
# Print out a message when the service gets invoked.
#
import sys
from rvilib import RVI

def usage():
    print "Usage:", sys.argv[0], "<rvi_url> <service_name>"
    print "  <rvi_url>                     URL of Service Edge on a local RVI node"
    print "  <service_name>                URL of Service to register"
    print
    print "The RVI Service Edge URL can be found in"
    print "[backend,vehicle].config as"
    print "env -> rvi -> components -> service_edge -> url"
    print
    print "The Service Edge URL is also logged as a notice when the"
    print "RVI node is started."
    print
    print "Example: ./rvi_service.py http://rvi1.nginfotpdx.net:8801 /test/some_service"
    sys.exit(255)


#
# Our general handler, registered with rvi.register_service() below.
#
# You can also explicitly name the arguments, but then
# the sender has to match the argument names.

# For example:
# rvi_call.py http://localhost:8801 jlr.com/vin/test a=1 b=2 c=3 ->
#    def service(a,b,c)
# 
def service_invoked(**args):
    print
    print "Service invoked!"
    print "args:", args 
    print
    sys.stdout.write("Press enter to quit: ")
    sys.stdout.flush()
    return ['ok']

def services_available(services):
    print
    print "Services available: ", services
    sys.stdout.write("Press enter to quit: ")
    sys.stdout.flush()

    return ['ok']

def services_unavailable(services):
    print
    print "Services not available: ", services

    sys.stdout.write("Press enter to quit: ")
    sys.stdout.flush()
    return ['ok']

if len(sys.argv) != 3:
    usage()

# Grab the URL to use
[ progname, rvi_node_url, service_name ] = sys.argv    


# Setup a connection to the local RVI node
rvi = RVI(rvi_node_url)

# Starting the thread that handles incoming calls is
# not really necessary since register_service will do it for us.

rvi.start_serve_thread() 

# Register our service  and invoke 'service_invoked' if we 
# get an incoming JSON-RPC call to it from the RVI node
#
full_service_name = rvi.register_service(service_name, service_invoked) 

# Tie callbacks to be invoked as the RVI node reports to us
# about other services being available.
rvi.set_services_available_callback(services_available)
rvi.set_services_unavailable_callback(services_unavailable)

print "RVI General Service."
print "RVI node URL:        ", rvi_node_url
print "Service:             ", full_service_name

raw_input('Press enter to quit: ')
rvi.shutdown()
sys.exit(0)
