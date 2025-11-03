"""
Servidor HTTP simple para servir el dashboard HTML.
Permite visualizar el dashboard en el navegador con las imágenes y datos.
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000

class ETLHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado para servir archivos con CORS habilitado."""
    
    def end_headers(self):
        # Habilitar CORS para permitir cargar recursos locales
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Personalizar los mensajes de log."""
        print(f"[SERVIDOR] {args[0]}")

def main():
    """Inicia el servidor HTTP para el dashboard."""
    # Cambiar al directorio raíz del proyecto (subir dos niveles desde scripts_project)
    project_root = Path(__file__).parent.parent.absolute()
    os.chdir(project_root)
    
    with socketserver.TCPServer(("", PORT), ETLHandler) as httpd:
        print("=" * 70)
        print(" SERVIDOR DASHBOARD ETL")
        print("=" * 70)
        print(f"\n✓ Servidor iniciado en puerto {PORT}")
        print(f"✓ Directorio raíz: {project_root}")
        print(f"\n🌐 Abriendo dashboard en el navegador...")
        print(f"\n📍 URL: http://localhost:{PORT}/dashboard/dashboard.html")
        print("\n⚠ Presiona Ctrl+C para detener el servidor")
        print("=" * 70 + "\n")
        
        # Abrir el navegador automáticamente
        try:
            webbrowser.open(f'http://localhost:{PORT}/dashboard/dashboard.html')
        except:
            print("⚠ No se pudo abrir el navegador automáticamente.")
            print("   Abre manualmente: http://localhost:8000/dashboard/dashboard.html")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Servidor detenido. ¡Hasta luego!")

if __name__ == "__main__":
    main()

