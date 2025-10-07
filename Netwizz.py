import os
import sys
import subprocess
import json
import time
import socket
from shutil import which

# ---------------------------
# Funciones utilitarias
# ---------------------------

def banner():
    print(r"""
███╗   ██╗███████╗████████╗██╗    ██╗██╗███████╗███████╗
████╗  ██║██╔════╝╚══██╔══╝██║    ██║██║╚══███╔╝╚══███╔╝
██╔██╗ ██║█████╗     ██║   ██║ █╗ ██║██║  ███╔╝   ███╔╝ 
██║╚██╗██║██╔══╝     ██║   ██║███╗██║██║ ███╔╝   ███╔╝  
██║ ╚████║███████╗   ██║   ╚███╔███╔╝██║███████╗███████╗
          --------------------------------------------
          Herramienta de automatización de escaneos
          --------------------------------------------          
                    Coded by: retr0bit
                    GitHub: github.com/retr0-bit011
                    [!] Leer README
    """)


def show_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "No se pudo obtener la IP"
    print(f"[+] IP local detectada: {ip}\n")

# ---------------------------
# Funciones para aircrack-ng
# ---------------------------

def list_interfaces():
    print("[+] Detectando interfaces inalámbricas...")
    try:
        result = subprocess.run(["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("[!] iwconfig no está instalado. Instala wireless-tools.")

def set_monitor_mode(interface):
    try:
        print(f"[+] Desactivando {interface}...")
        subprocess.run(["ifconfig", interface, "down"], check=True)
        print(f"[+] Poniendo {interface} en modo monitor...")
        subprocess.run(["iwconfig", interface, "mode", "monitor"], check=True)
        subprocess.run(["ifconfig", interface, "up"], check=True)
        print(f"[+] {interface} ahora está en modo monitor.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al configurar {interface}: {e}")

def run_airodump(interface, outfile_prefix):
    print("[+] Iniciando airodump-ng...")
    print("[+] Presiona Ctrl+C para detener el escaneo.\n")
    try:
        subprocess.run([
            "airodump-ng",
            "--write", outfile_prefix,
            "--output-format", "pcap,csv",
            interface
        ])
    except KeyboardInterrupt:
        print("\n[+] Escaneo detenido por el usuario.")
    print(f"[+] Resultados guardados con prefijo: {outfile_prefix}")

def aircrack_menu():
    while True:
        print("\n[+] Aircrack-ng Suite:")
        print("   1) Listar interfaces inalámbricas")
        print("   2) Poner interfaz en modo monitor")
        print("   3) Ejecutar airodump-ng")
        print("   4) Volver al menú principal")
        choice = input("[+] Selecciona opción: ").strip()

        if choice == "1":
            list_interfaces()
        elif choice == "2":
            iface = input("[+] Ingresa interfaz a poner en monitor: ").strip()
            set_monitor_mode(iface)
        elif choice == "3":
            iface = input("[+] Ingresa interfaz en modo monitor: ").strip()
            outfile = input("[+] Ingresa nombre base para guardar resultados: ").strip()
            run_airodump(iface, outfile)
        elif choice == "4":
            break
        else:
            print("[!] Opción inválida.")

# ---------------------------
# Funciones de escaneo (masscan + nmap)
# ---------------------------

def run_external_tool(tool, args=None, out_dir="outputs"):
    if not which(tool):
        print(f"[!] No se encontró '{tool}' en el PATH.")
        return None

    if args is None:
        args = []

    os.makedirs(out_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    txt_out = os.path.join(out_dir, f"{tool}_{timestamp}.txt")
    json_out = os.path.join(out_dir, f"{tool}_{timestamp}.json")

    print(f"[+] Ejecutando: {tool} {' '.join(args)}")
    with open(txt_out, "w") as fout:
        proc = subprocess.run([tool] + args, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True)
        fout.write(proc.stdout)

    record = {
        "tool": tool,
        "args": args,
        "timestamp": timestamp,
        "returncode": proc.returncode,
        "output_file": txt_out
    }
    with open(json_out, "w") as jf:
        json.dump(record, jf, indent=4)

    print(f"[+] Salida guardada en {txt_out}")
    return record

def run_masscan(target, ports="1-1000", rate="1000"):
    return run_external_tool("masscan", ["-p", ports, target, "--rate", rate, "--wait", "0"], out_dir="masscan_outputs")

def run_nmap(target, options=None):
    if options is None:
        options = ["-sV", "-O"]
    return run_external_tool("nmap", options + [target], out_dir="nmap_outputs")

def interactive_mode():
    target = input("[+] Ingresa el rango a escanear: ").strip()
    print("[+] Selecciona tipo de escaneo:")
    print("   1) Rápido (puertos comunes)")
    print("   2) Completo (todos los puertos)")
    print("   3) Personalizado")
    opt = input("[+] Opción: ").strip()

    if opt == "1":
        run_nmap(target, ["-T5", "-F"])
    elif opt == "2":
        run_nmap(target, ["-p-", "-sV", "-O"])
    elif opt == "3":
        custom = input("[+] Ingresa las flags para nmap: ").strip().split()
        run_nmap(target, custom)
    else:
        print("[!] Opción inválida.")

def automated_mode_from_file():
    filename = input("[+] Archivo con lista de objetivos: ").strip()
    if not os.path.isfile(filename):
        print("[!] Archivo no encontrado.")
        return
    with open(filename) as f:
        targets = [line.strip() for line in f if line.strip()]
    for t in targets:
        run_masscan(t)
        run_nmap(t)

# ---------------------------
# Main
# ---------------------------

def main():
    banner()
    show_ip()
    while True:
        print("[+] Menú principal:")
        print("   1) Escaneo interactivo (nmap/masscan)")
        print("   2) Escaneo automatizado desde archivo")
        print("   3) Aircrack-ng suite")
        print("   4) Salir")
        modo = input("[+] Elige una opción: ").strip()
        if modo == "1":
            interactive_mode()
        elif modo == "2":
            automated_mode_from_file()
        elif modo == "3":
            aircrack_menu()
        elif modo == "4":
            print("[+] Saliendo...")
            break
        else:
            print("[!] Opción inválida.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[+] Saliendo por Ctrl+C...")


