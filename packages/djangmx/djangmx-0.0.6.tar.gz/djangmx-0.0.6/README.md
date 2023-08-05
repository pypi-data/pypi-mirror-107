# djangmx
handles communications between django and AMX via UDP

## udp_to_amx(amx_ip, amx_rx_port, message):
### amx_ip: (string)
#### IP address of the AMX master you're sending the message to.
### amx_rx_port: (integer default 10002)
#### UDP port the AMX master will be listening on. This module does not listen for responses on this port.
### message: (string)
#### Message to send to the AMX master


## amx_to_django_listener(server_ip, server_rx_port, django_ip, django_port):
### server_ip: (string)
#### IP address of the server that will be handling communications from AMX to django.
### server_rx_port: (integer default 10004)
#### Port the server will listen on. "ACK\r" will be sent to AMX when messages are received.
### django_ip: (string)
#### IP address of the django server. This may or may not be the same as server_ip
### django_port: (integer default 8000)
#### Port that django's http server is running on. This must not match server_rx_port.


If an AMX master sends a message with 'get_id' in it, the listener created by amx_to_django_listener() will http GET to:
http://django_ip:django_port/equipment/get_id/<i>ip of the master that sent the message</i>

The django server will be configured to use udp_to_amx() to send the django IDs of all registered equipment associated with that AMX master.

The AMX program assigns these IDs to the device structures in its programs, and these IDs will then be used in all status updates from the AMX master.

The header used by AMX in these status updates is ':::' The delimiter is '~' with a '~' on the end.
Example status update of a projector:    <i>:::35672~True~Warming Up~Online~1244~</i>
The value and expected order of each <i>parameter~</i> is handled in the AMX program and parsing within your django project.
Status messages from AMX can be strung together, as long as each message begins with <i>:::</i>
The listener created by amx_to_django_listener() will separate the messages and http GET them to:
http://django_ip:django_port/equipment/amx_fb/<i>message</i>
Handling of this message will be done in your django project.
