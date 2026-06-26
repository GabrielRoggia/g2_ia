import matplotlib
matplotlib.use("Agg")  # headless — funciona sem display
import matplotlib.pyplot as plt

from .city import City


def plot_route(
    cities: list[City],
    route: list[int],
    title: str = "Melhor Rota TSP",
    save_path: str | None = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 8))

    ordered = [cities[i] for i in route] + [cities[route[0]]]
    xs = [c.x for c in ordered]
    ys = [c.y for c in ordered]
    ax.plot(xs, ys, "b-", linewidth=1.5, zorder=1, alpha=0.7)

    ax.scatter(
        [c.x for c in cities],
        [c.y for c in cities],
        c="red",
        s=80,
        zorder=2,
    )
    ax.scatter([cities[route[0]].x], [cities[route[0]].y], c="green", s=120, zorder=3, label="Início")

    for i, city in enumerate(cities):
        ax.annotate(
            str(i),
            (city.x, city.y),
            textcoords="offset points",
            xytext=(6, 4),
            fontsize=8,
        )

    ax.set_title(title, fontsize=13)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)

    return fig


def plot_evolution(
    history: list[float],
    title: str = "Evolução da Melhor Distância por Geração",
    save_path: str | None = None,
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(history, color="steelblue", linewidth=1.5)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("Geração")
    ax.set_ylabel("Distância Total")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_population(
    distances: list[float],
    generation: int,
    elitism: int = 5,
    save_path: str | None = None,
) -> plt.Figure:
    """Gráfico de barras da população ordenada do pior ao melhor."""
    n = len(distances)
    sorted_dists = sorted(distances, reverse=True)  # pior → melhor (esquerda → direita)

    colors = []
    for i in range(n):
        if i < n - elitism:
            colors.append("#e05c5c")   # vermelho — descartados
        else:
            colors.append("#4caf50")   # verde — elite preservada

    fig, ax = plt.subplots(figsize=(max(8, n * 0.5), 5))
    bars = ax.bar(range(1, n + 1), sorted_dists, color=colors, edgecolor="white", linewidth=0.5)

    # Rótulos de valor em cada barra
    for bar, dist in zip(bars, sorted_dists):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (max(sorted_dists) - min(sorted_dists)) * 0.01,
            f"{dist:.0f}",
            ha="center", va="bottom", fontsize=7, rotation=90,
        )

    ax.set_title(f"Geração {generation} — População ordenada do pior ao melhor", fontsize=12)
    ax.set_xlabel("Indivíduo (1 = pior → N = melhor)")
    ax.set_ylabel("Distância total da rota")
    ax.set_xticks(range(1, n + 1))
    ax.grid(axis="y", alpha=0.3)

    from matplotlib.patches import Patch
    legend = [
        Patch(color="#e05c5c", label="Descartado"),
        Patch(color="#4caf50", label=f"Elite (top {elitism}) — preservado"),
    ]
    ax.legend(handles=legend, loc="upper right")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return fig
