import nmap

# Initialize the port scanner
nmScan = nmap.PortScanner()

# Scan localhost for ports in range 21-443
nmScan.scan('127.0.0.1', '21-443')

# run a loop to print all found result about the ports
for host in nmScan.all_hosts():
  print("Host: %s (%s)" % (host, nmScan[host].hostname()))
  print("State: %s" % nmScan[host].state())
  for proto in nmScan[host].all_protocols():
    print("-----------")
    print("Protocol: %s" % proto)

    lport = sorted(nmScan[host][proto].keys())
    for port in lport:
      print("port: %s\tstate : %s" % (port, nmScan[host][proto][port]['state']))
        