import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

def agrupar_e_plotar(itens, atributo):
    contagem = Counter(item[atributo] for item in itens if atributo in item and item[atributo])
    if not contagem:
        return None

    labels, valores = zip(*contagem.items())
    fig, ax = plt.subplots()
    ax.barh(labels, valores)
    ax.set_xlabel("Quantidade")
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode()
