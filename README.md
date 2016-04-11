# http-proxy-handler-request
The software is a light proxy http and it allows you to analyze the traffic between a web browser and the web server. Furthermore, you can modify the request as you wish and submit the modify one to the remote web server. You can modify every information passed through the request such as user-agent, cookie, host, etc.

[Requirments]

python 2.7 or greater


[Usage]

python proxy.py 9000

You can change the port where the proxy is listen to. The port must be greater than 1023 for this reason: http://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml

1) Start the http proxy

2) Configure a web browser to use it (you can find this option inside the settings of a web browser)

3) You do a request and it is written inside the file handlerequest.conf and the software waits.

4) If you want to modify the request you can open handlerequest.conf file, make the necessary changes, and restart the proxy by pressing a button in the terminal where you started the proxy. Automatically, the new request is submitted to the remote web server.


Developed by Alessandro Peretti
