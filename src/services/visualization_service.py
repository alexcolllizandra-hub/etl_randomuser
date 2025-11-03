import matplotlib.pyplot as plt
from collections import Counter
import os
from src.models.user_model import User

plt.style.use("default")

class VisualizationService:
    """Visualizaciones descriptivas y analíticas de usuarios."""

    def __init__(self, output_dir: str = "plots"):
        """Inicializa el servicio de visualización con directorio de salida."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_age_distribution(self, users: list[User]) -> None:
        if not users:
            print("No hay datos para generar gráfico de distribución de edades.")
            return
        
        ages = [u.age for u in users]
        plt.figure(figsize=(8, 5))
        plt.hist(ages, bins=15, color="#1f77b4", edgecolor="black", alpha=0.7)
        plt.title("Distribución de Edades")
        plt.xlabel("Edad")
        plt.ylabel("Frecuencia")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, "distribucion_edades.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {filepath}")
        plt.show()

    def plot_gender_distribution(self, users: list[User]) -> None:
        if not users:
            print("No hay datos para generar gráfico de distribución por género.")
            return
        
        gender_counts = Counter(u.gender for u in users)
        genders = list(gender_counts.keys())
        counts = list(gender_counts.values())
        colors = ["#66c2a5", "#fc8d62"]
        
        plt.figure(figsize=(6, 4))
        plt.bar(genders, counts, color=colors[:len(genders)])
        plt.title("Distribución por Género")
        plt.xlabel("Género")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, "distribucion_genero.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {filepath}")
        plt.show()

    def plot_top_countries(self, users: list[User], top_n: int = 10) -> None:
        if not users:
            print("No hay datos para generar gráfico de países.")
            return
        
        country_counts = Counter(u.country for u in users)
        top_countries = country_counts.most_common(top_n)
        countries = [c[0] for c in top_countries]
        counts = [c[1] for c in top_countries]
        
        plt.figure(figsize=(9, 6))
        plt.barh(countries, counts, color="#4a90e2")
        plt.title(f"Top {top_n} Países con más Usuarios")
        plt.xlabel("Cantidad")
        plt.ylabel("País")
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, "top_paises.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {filepath}")
        plt.show()

    def plot_age_by_country(self, users: list[User], top_n: int = 6):
        """Muestra la distribución de edad por país con boxplots."""
        if not users:
            print("No hay datos para generar gráfico de edad por país.")
            return
        
        country_counts = Counter(u.country for u in users)
        top_countries = [c[0] for c in country_counts.most_common(top_n)]
        
        # Agrupar edades por país
        age_by_country = {country: [] for country in top_countries}
        for u in users:
            if u.country in top_countries:
                age_by_country[u.country].append(u.age)
        
        # Preparar datos para matplotlib
        data = [age_by_country[country] for country in top_countries]
        
        plt.figure(figsize=(10, 6))
        bp = plt.boxplot(data, labels=top_countries, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('#b3d9ff')
        plt.title(f"Distribución de Edad por País (Top {top_n})")
        plt.xlabel("País")
        plt.ylabel("Edad")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, "edad_por_pais.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {filepath}")
        plt.show()

    def plot_correlation_matrix(self, users: list[User]):
        """Matriz de correlación entre variables numéricas."""
        if not users:
            print("No hay datos para generar matriz de correlación.")
            return
        
        # Extraer solo variables numéricas
        ages = [u.age for u in users]
        numeric_data = {"age": ages}
        
        # Añadir variables numéricas adicionales si existen
        if hasattr(users[0], 'population') and users[0].population:
            numeric_data["population"] = [u.population for u in users]
        if hasattr(users[0], 'is_outlier'):
            numeric_data["is_outlier"] = [1 if u.is_outlier else 0 for u in users]
        
        if len(numeric_data) < 2:
            print("No hay suficientes variables numéricas para correlación.")
            return
        
        # Calcular matriz de correlación manualmente
        labels = list(numeric_data.keys())
        n = len(labels)
        corr_matrix = [[0.0] * n for _ in range(n)]
        
        # Función para calcular correlación manualmente
        def _correlation(x, y):
            n = len(x)
            if n == 0:
                return 0.0
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            
            numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
            sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
            sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
            denominator = (sum_sq_x * sum_sq_y) ** 0.5
            
            if denominator == 0:
                return 0.0
            return numerator / denominator
        
        for i, label1 in enumerate(labels):
            for j, label2 in enumerate(labels):
                if i == j:
                    corr_matrix[i][j] = 1.0
                else:
                    corr_matrix[i][j] = _correlation(numeric_data[label1], numeric_data[label2])
        
        plt.figure(figsize=(6, 5))
        im = plt.imshow(corr_matrix, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)
        plt.colorbar(im)
        plt.xticks(range(n), labels, rotation=45, ha="right")
        plt.yticks(range(n), labels)
        plt.title("Matriz de Correlación")
        
        # Anotar valores
        for i in range(n):
            for j in range(n):
                plt.text(j, i, f"{corr_matrix[i][j]:.2f}", ha="center", va="center", color="black")
        
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, "matriz_correlacion.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {filepath}")
        plt.show()
