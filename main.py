from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Port & Service Lookup API",
    description="API para consultar puertos de red",
    version="1.0.0"
)

PORTS_DB = {
    20: {"service": "FTP-DATA", "protocol": "TCP", "risk": "Medio", "desc": "Transferencia de datos FTP no cifrada."},
    21: {"service": "FTP", "protocol": "TCP", "risk": "Alto", "desc": "Control FTP."},
    22: {"service": "SSH", "protocol": "TCP", "risk": "Bajo", "desc": "Secure Shell."},
    23: {"service": "TELNET", "protocol": "TCP", "risk": "Alto", "desc": "Consola remota sin cifrado."},
    25: {"service": "SMTP", "protocol": "TCP", "risk": "Medio", "desc": "Envio de correo."},
    53: {"service": "DNS", "protocol": "TCP/UDP", "risk": "Bajo", "desc": "Domain Name System."},
    80: {"service": "HTTP", "protocol": "TCP", "risk": "Medio", "desc": "Trafico web no cifrado."},
    443: {"service": "HTTPS", "protocol": "TCP", "risk": "Bajo", "desc": "Trafico web cifrado SSL/TLS."},
    445: {"service": "SMB", "protocol": "TCP", "risk": "Alto", "desc": "Comparticion de archivos Windows."},
    3306: {"service": "MySQL", "protocol": "TCP", "risk": "Medio", "desc": "Base de datos MySQL."},
    3389: {"service": "RDP", "protocol": "TCP", "risk": "Alto", "desc": "Remote Desktop Protocol."},
    8080: {"service": "HTTP-ALT", "protocol": "TCP", "risk": "Medio", "desc": "Servidor web alternativo."}
}

@app.get("/")
def root():
    return {"message": "Port Lookup API is Live", "docs": "/docs"}

@app.get("/api/v1/port/{port_number}")
def get_port_info(port_number: int):
    if port_number in PORTS_DB:
        return {"status": "success", "port": port_number, "data": PORTS_DB[port_number]}
    raise HTTPException(status_code=404, detail="Puerto no registrado")
