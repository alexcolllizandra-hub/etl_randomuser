# -*- coding: utf-8 -*-
"""
Pipeline completo: Ejecuta el ETL y luego verifica la base de datos SQLite
"""
import os
import sys
import subprocess
import sqlite3

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70 + "\n")

def run_etl():
    """Ejecuta el proceso ETL completo."""
    print_header("ETAPA 1: EJECUTANDO PROCESO ETL")
    
    # Verificar que existe el módulo main
    if not os.path.exists("src/main.py"):
        print("ERROR: No se encuentra src/main.py")
        return False
    
    try:
        # Ejecutar el ETL
        result = subprocess.run(
            [sys.executable, "-m", "src.main"],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("\n✓ Proceso ETL completado exitosamente")
            return True
        else:
            print("\n✗ Error en el proceso ETL")
            return False
            
    except Exception as e:
        print(f"\n✗ Error al ejecutar ETL: {e}")
        return False

def verify_sqlite():
    """Verifica que la base de datos SQLite funcione correctamente."""
    print_header("ETAPA 2: VERIFICACIÓN DE BASE DE DATOS SQLITE")
    
    db_path = "data/usuarios.db"
    
    # Verificar que existe la base de datos
    if not os.path.exists(db_path):
        print(f"ERROR: No se encuentra la base de datos en {db_path}")
        print("Por favor ejecuta primero el ETL")
        return False
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Listar tablas
        print("1. Verificando tablas en la base de datos:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if not tables:
            print("   ✗ No se encontraron tablas")
            conn.close()
            return False
        
        for table in tables:
            print(f"   ✓ Tabla encontrada: {table[0]}")
        
        # 2. Verificar estructura de la tabla users
        if ('users',) in tables:
            print("\n2. Verificando estructura de la tabla 'users':")
            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()
            
            print("   Columnas encontradas:")
            for col in columns:
                print(f"   - {col[1]} ({col[2]})")
        
        # 3. Contar total de usuarios
        print("\n3. Verificando datos:")
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        print(f"   ✓ Total de usuarios: {total}")
        
        if total == 0:
            print("   ⚠ Advertencia: No hay usuarios en la base de datos")
        elif total < 10:
            print(f"   ⚠ Advertencia: Solo hay {total} usuarios (esperabas más?)")
        
        # 4. Verificar distribución por género
        print("\n4. Verificando distribución por género:")
        cursor.execute("SELECT gender, COUNT(*) as count FROM users GROUP BY gender")
        gender_dist = cursor.fetchall()
        
        for gender, count in gender_dist:
            print(f"   - {gender}: {count} usuarios ({count*100/total:.1f}%)")
        
        # 5. Top 5 países
        print("\n5. Top 5 países más representados:")
        cursor.execute("""
            SELECT country, COUNT(*) as count 
            FROM users 
            GROUP BY country 
            ORDER BY count DESC 
            LIMIT 5
        """)
        countries = cursor.fetchall()
        
        for i, (country, count) in enumerate(countries, 1):
            print(f"   {i}. {country}: {count} usuarios")
        
        # 6. Estadísticas de edad
        print("\n6. Estadísticas de edad:")
        cursor.execute("""
            SELECT 
                MIN(age) as min_age,
                MAX(age) as max_age,
                CAST(AVG(age) AS FLOAT) as avg_age
            FROM users
        """)
        stats = cursor.fetchone()
        
        if stats and stats[2]:  # Si avg_age no es None
            print(f"   - Edad mínima: {stats[0]} años")
            print(f"   - Edad máxima: {stats[1]} años")
            print(f"   - Edad promedio: {stats[2]:.2f} años")
        else:
            print("   ⚠ No se pudieron calcular estadísticas de edad")
        
        # 7. Ejemplo de consulta compleja
        print("\n7. Ejecutando consulta compleja (rangos de edad):")
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN age < 18 THEN 'Menores'
                    WHEN age < 25 THEN '18-24'
                    WHEN age < 35 THEN '25-34'
                    WHEN age < 45 THEN '35-44'
                    WHEN age < 55 THEN '45-54'
                    WHEN age < 65 THEN '55-64'
                    WHEN age < 75 THEN '65-74'
                    ELSE '75+'
                END as age_range,
                COUNT(*) as count
            FROM users
            GROUP BY age_range
            ORDER BY 
                CASE age_range
                    WHEN 'Menores' THEN 0
                    WHEN '18-24' THEN 1
                    WHEN '25-34' THEN 2
                    WHEN '35-44' THEN 3
                    WHEN '45-54' THEN 4
                    WHEN '55-64' THEN 5
                    WHEN '65-74' THEN 6
                    ELSE 7
                END
        """)
        age_ranges = cursor.fetchall()
        
        for age_range, count in age_ranges:
            print(f"   - {age_range}: {count} usuarios")
        
        # 8. Verificar integridad de datos
        print("\n8. Verificando integridad de datos:")
        cursor.execute("SELECT COUNT(*) FROM users WHERE email IS NULL OR email = ''")
        null_emails = cursor.fetchone()[0]
        print(f"   - Registros sin email: {null_emails}")
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE age IS NULL OR age <= 0")
        invalid_ages = cursor.fetchone()[0]
        print(f"   - Registros con edad inválida: {invalid_ages}")
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE country IS NULL OR country = ''")
        null_countries = cursor.fetchone()[0]
        print(f"   - Registros sin país: {null_countries}")
        
        conn.close()
        
        print_header("ETAPA 2 COMPLETADA: Base de datos verificada exitosamente")
        return True
        
    except sqlite3.Error as e:
        print(f"\n✗ Error de SQLite: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        return False

def verify_csv():
    """Verifica que el archivo CSV se haya generado correctamente."""
    print_header("ETAPA 3: VERIFICACIÓN DE ARCHIVO CSV")
    
    csv_path = "data/usuarios.csv"
    
    if not os.path.exists(csv_path):
        print(f"ERROR: No se encuentra el archivo CSV en {csv_path}")
        return False
    
    try:
        # Leer el archivo CSV
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("   ✗ El archivo CSV está vacío")
            return False
        
        print(f"   ✓ Archivo CSV encontrado: {csv_path}")
        print(f"   ✓ Total de líneas: {len(lines)}")
        print(f"   ✓ Primera línea (header): {lines[0].strip()}")
        
        if len(lines) > 1:
            print(f"   ✓ Primera fila de datos: {lines[1].strip()[:80]}...")
        else:
            print("   ⚠ Solo hay encabezado, no hay datos")
        
        print_header("ETAPA 3 COMPLETADA: Archivo CSV verificado")
        return True
        
    except Exception as e:
        print(f"\n✗ Error al verificar CSV: {e}")
        return False

def verify_plots():
    """Verifica que se hayan generado los gráficos."""
    print_header("ETAPA 4: VERIFICACIÓN DE GRÁFICOS")
    
    plots_dir = "plots"
    expected_plots = [
        "distribucion_edades.png",
        "distribucion_genero.png",
        "top_paises.png",
        "edad_por_pais.png",
        "matriz_correlacion.png"
    ]
    
    if not os.path.exists(plots_dir):
        print(f"ERROR: No se encuentra el directorio {plots_dir}")
        return False
    
    print(f"Buscando gráficos en: {plots_dir}/")
    found_plots = []
    
    for plot in expected_plots:
        plot_path = os.path.join(plots_dir, plot)
        if os.path.exists(plot_path):
            size = os.path.getsize(plot_path)
            print(f"   ✓ {plot} ({size:,} bytes)")
            found_plots.append(plot)
        else:
            print(f"   ✗ {plot} - NO ENCONTRADO")
    
    if len(found_plots) == len(expected_plots):
        print_header("ETAPA 4 COMPLETADA: Todos los gráficos generados")
        return True
    else:
        print(f"\n⚠ Advertencia: Solo se encontraron {len(found_plots)} de {len(expected_plots)} gráficos")
        return False

def main():
    """Pipeline principal que ejecuta el ETL y todas las verificaciones."""
    import sys
    
    # Verificar si se debe saltar el ETL
    skip_etl = "--skip-etl" in sys.argv or "-s" in sys.argv
    
    print_header("PIPELINE COMPLETO: ETL + VERIFICACIONES")
    
    # Ejecutar ETL (a menos que se especifique --skip-etl)
    if skip_etl:
        print("Omitiendo ejecución del ETL (--skip-etl)")
        etl_success = True
    else:
        etl_success = run_etl()
        
        if not etl_success:
            print_header("PIPELINE FALLIDO: El proceso ETL terminó con errores")
            return False
    
    # Verificar resultados
    csv_success = verify_csv()
    sqlite_success = verify_sqlite()
    plots_success = verify_plots()
    
    # Resumen final
    print_header("RESUMEN FINAL DEL PIPELINE")
    
    results = [
        ("ETL", etl_success),
        ("CSV", csv_success),
        ("SQLite", sqlite_success),
        ("Gráficos", plots_success)
    ]
    
    all_success = True
    for name, success in results:
        status = "✓ ÉXITO" if success else "✗ FALLIDO"
        print(f"{name:20} : {status}")
        if not success:
            all_success = False
    
    print("\n" + "=" * 70)
    if all_success:
        print(" ✓ PIPELINE COMPLETADO EXITOSAMENTE")
    else:
        print(" ✗ PIPELINE COMPLETADO CON ERRORES")
    print("=" * 70 + "\n")
    
    return all_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

