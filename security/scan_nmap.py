import nmap
import argparse

def nmapScan(tgtHost, tgtPort):
  nmscan = nmap.PortScanner()
  nmscan.scan(tgtHost, tgtPort)
  state = nmscan[tgtHost]['tcp'][int(tgtPort)]['state']
  print(" [*] " + tgtHost + " tcp/" + tgtPort + " "+state)

def main():
  parser = argparse.ArgumentParser(description='Comman line argument parsing')

  parser.add_argument('--host', action='store', dest='host', required=True)
  parser.add_argument('--port', action='store', dest='port', required=True)

  given_args = parser.parse_args()
  tgtHost = given_args.host
  tgtPort = given_args.port

  if(tgtHost == None or tgtPort == None):
    print(parser.usage)
    exit(0)
  else:
    print("Scanning: " + tgtHost + "-" + str(tgtPort))
    nmapScan(tgtHost, str(tgtPort))

if __name__ == '__main__':
  main()