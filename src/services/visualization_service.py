import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from src.models.user_model import User

plt.style.use("ggplot")

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
        df = pd.DataFrame([u.__dict__ for u in users])
        plt.figure(figsize=(8, 5))
        sns.histplot(df["age"], bins=15, kde=True, color="#1f77b4")
        plt.title("Distribución de Edades")
        plt.xlabel("Edad")
        plt.ylabel("Frecuencia")
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, "distribucion_edades.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {filepath}")
        plt.show()

    def plot_gender_distribution(self, users: list[User]) -> None:
        if not users:
            print("No hay datos para generar gráfico de distribución por género.")
            return
        df = pd.DataFrame([u.__dict__ for u in users])
        plt.figure(figsize=(6, 4))
        sns.countplot(x="gender", data=df, hue="gender", palette="Set2", legend=False)
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
        df = pd.DataFrame([u.__dict__ for u in users])
        top_countries = df["country"].value_counts().head(top_n)
        plt.figure(figsize=(9, 6))
        sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.values, palette="Blues_d", legend=False)
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
        df = pd.DataFrame([u.__dict__ for u in users])
        top = df["country"].value_counts().nlargest(top_n).index
        subset = df[df["country"].isin(top)]
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=subset, x="country", y="age", hue="country", palette="Pastel1", legend=False)
        plt.title(f"Distribución de Edad por País (Top {top_n})")
        plt.xticks(rotation=45)
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
        df = pd.DataFrame([u.__dict__ for u in users])
        numeric_cols = df.select_dtypes(include=["int", "float"])
        if numeric_cols.empty:
            print("No hay variables numéricas para correlación.")
            return
        corr = numeric_cols.corr()
        plt.figure(figsize=(6, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matriz de Correlación")
        plt.tight_layout()
        filepath = os.path.join(self.output_dir, "matriz_correlacion.png")
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Gráfico guardado en: {filepath}")
        plt.show()
