# Netwizz
This tool integrates network scanning functions (nmap, masscan) and the Aircrack-ng suite (Airodump) for wireless audits.
The goal is to centralize common pentesting tasks into a single interactive menu, streamlining the workflow.

## Disclaimer: This tool is for educational purposes only and for auditing purposes on your own networks or with explicit authorization.
Misuse may be illegal.

## Features:

### Network Scanning: 
- Quick scan with Nmap (common ports).
- Full scan (all ports).
- Custom scan with selectable flags.
- Integration with Masscan for rapid discovery.
  
### Aircrack-ng Suite:
- List wireless interfaces.
- Place interface in monitor mode.
- Run airodump-ng to capture wireless traffic, with results in .pcap and .csv.

### Utilities:
- Local IP detection.
- Automatic saving of outputs in organized folders (nmap_outputs/, masscan_outputs/, airodump_outputs/).
- Results also in JSON format with execution metadata.

### Output Structure:
- nmap_outputs/ → Nmap outputs (.txt, .json)
- masscan_outputs/ → Masscan results (.txt, .json)
- airodump_outputs/ → Airodump Captures (.cap, .csv)

### Requirements:
- Python 3.7+
- Linux-only script
- Installed external tools:
      - nmap
      - masscan
      - aircrack-ng
      - wireless-tools
### How to use:
- Run the script (with root)
  ```bash
  sudo python3 Netwizz.py

- Main Menu:
  1) Escaneo interactivo (nmap/masscan)
  2) Escaneo automatizado desde archivo
  3) Aircrack-ng suite
  4) Salir

### Captures
![Foto 1](https://github.com/user-attachments/assets/e2fe8c41-f224-4ef0-b87b-3e2e358e1af8)


![Foto2](https://github.com/user-attachments/assets/eb01a976-3a1d-4e00-98aa-748c72490e32)


- Author
retr0bit
- GitHub: github.com/retr0-bit011


