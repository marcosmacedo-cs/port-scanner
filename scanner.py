import socket
import threading
import json
import argparse
from queue import Queue
from datetime import datetime

open_ports = []
q = Queue()

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            try:
                sock.send("Olá\r\n")
                banner = sock.recv(1024).decode(errors="ignorar").strip()
            except:
                banner = "Nenhum banner"
            open_ports.append({"port":port, "banner":banner})
            print(f"Porta {port} aberta: {banner}")
        sock.lose()
    except Exception as e:
        pass

def threarder(host):
    while not q.empty():
        port = q.get()
        scan_port(host, port)
        q.task_done()

def run_scan(host, start_port, end_port, threads, output):
    start_time = datetime.now()
    print(f"Iniciando varredura em {host} de {start_port} a {end_port} com {threads} threads...\n")
    for port in range(start_port, end_port + 1):
        q.put(port)
    for _ in range(threads):
        t = threading.Thread(target=threarder, args=(host,))
        t.daemon = True
        t.start()
    q.join()
    duration = (datetime.now() - start_time).total_seconds()
    print(f"\nVarredura concluída em {duration} segundos.")
    print(f"Portas abertas: {len(open_ports)}")
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(open_ports, f, indent=4)
        print(f"Resultados salvos em {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini Port Scanner 🛡️")
    parser.add_argument("host", help="Endereço IP ou hostname do alvo")
    parser.add_argument("--start", type=int, default=1, help="Porta inicial (padrão: 1)")
    parser.add_argument("--end", type=int, default=1024, help="Porta final (padrão: 1024)")
    parser.add_argument("--threads", type=int, default=50, help="Número de threads (padrão: 50)")
    parser.add_argument("--output", help="Arquivo JSON para salvar resultados (opcional)")
    parser.add_argument("--common", action="store_true", help="Scan rápido de portas comuns")
    args = parser.parse_args()

    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 8080]

    if args.common:
        print("Iniciando varredura rápida de portas comuns...")
        for port in common_ports:
            q.put(port)
        for _ in range(args.threads):
            t = threading.Thread(target=threarder, args=(args.host,))
            t.daemon = True
            t.start()
        q.join()
    else:
        run_scan(args.host, args.start, args.end, args.threads, args.output)