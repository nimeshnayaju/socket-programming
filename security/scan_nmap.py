import nmap
import optparse

def nmapScan(tgtHost, tgtPort):
  nmscan = nmap.PortScanner()
  nmscan.scan(tgtHost, tgtPort)
  state = nmscan[tgtHost]['tcp'][int(tgtPort)]['state']
  print(" [*] " + tgtHost + " tcp/" + tgtPort + " "+state)

def main():
  parser = optparse.OptionParser("Script Usage:" + "-H <target host> -p <target port>")
  parser.add_option("-H", dest="tgt_host", type="string", help="specify target host")
  parser.add_option("-p", dest="tgt_port", type="string", help="specify target port(s) separated by comma")

  (options, args) = parser.parse_args()
  tgtHost = options.tgt_host
  tgtPorts = str(options.tgt_port)

  if(tgtHost == None or tgtPorts == None):
    print(parser.usage)
    exit(0)
  
  ports = tgtPorts.strip("'").split(",")

  for tgtPort in ports:
    print(tgtHost + " - " + tgtPort)
    nmapScan(tgtHost, str(tgtPort))

if __name__ == '__main__':
  main()