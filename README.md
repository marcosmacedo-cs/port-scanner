# 🔍 Mini Port Scanner 🛡️

Um port scanner simples em **Python**, criado para fins educacionais.  
Permite verificar portas abertas em um host, com suporte a **multithreading**, **banner grabbing** e exportação em JSON.

---

## 🚀 Funcionalidades
- Escaneia uma faixa de portas.
- Modo rápido para **portas comuns** (21, 22, 80, 443, 3306...).
- **Multithreading** para acelerar o scan.
- **Banner grabbing** (tenta identificar o serviço na porta aberta).
- Exportação dos resultados em **JSON**.

---

## 📦 Instalação
```bash
git clone https://github.com/seu-usuario/port-scanner.git
cd port-scanner
python scanner.py --help