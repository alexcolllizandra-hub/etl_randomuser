import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from models.user_model import User

plt.style.use("ggplot")

class VisualizationService:
    """Visualizaciones descriptivas y analíticas de usuarios."""

    @staticmethod
    def plot_age_distribution(users: list[User]) -> None:
        df = pd.DataFrame([u.__dict__ for u in users])
        plt.figure(figsize=(8, 5))
        sns.histplot(df["age"], bins=15, kde=True, color="#1f77b4")
        plt.title("Distribución de Edades")
        plt.xlabel("Edad")
        plt.ylabel("Frecuencia")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_gender_distribution(users: list[User]) -> None:
        df = pd.DataFrame([u.__dict__ for u in users])
        plt.figure(figsize=(6, 4))
        sns.countplot(x="gender", data=df, palette="Set2")
        plt.title("Distribución por Género")
        plt.xlabel("Género")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_top_countries(users: list[User], top_n: int = 10) -> None:
        df = pd.DataFrame([u.__dict__ for u in users])
        top_countries = df["country"].value_counts().head(top_n)
        plt.figure(figsize=(9, 6))
        sns.barplot(x=top_countries.values, y=top_countries.index, palette="Blues_d")
        plt.title(f"Top {top_n} Países con más Usuarios")
        plt.xlabel("Cantidad")
        plt.ylabel("País")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_age_by_country(df: pd.DataFrame, top_n: int = 6):
        """Muestra la distribución de edad por país con boxplots."""
        top = df["country"].value_counts().nlargest(top_n).index
        subset = df[df["country"].isin(top)]
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=subset, x="country", y="age", palette="Pastel1")
        plt.title(f"Distribución de Edad por País (Top {top_n})")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_correlation_matrix(df: pd.DataFrame):
        """Matriz de correlación entre variables numéricas."""
        numeric_cols = df.select_dtypes(include=["int", "float"])
        corr = numeric_cols.corr()
        plt.figure(figsize=(6, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matriz de Correlación")
        plt.tight_layout()
        plt.show()
