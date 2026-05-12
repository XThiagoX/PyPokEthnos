import tkinter as tk
from controller import ControladorDoJogo
from view import TkinterView


def main():
    """Entrypoint de Bootstrapping do Padrao MVC."""
    # 1. Spawn Application Core
    root = tk.Tk()

    # 2. Injeta as Dependencias na Via Critica
    controlador = ControladorDoJogo()
    aplicativo = TkinterView(root, controlador)  # noqa: F841

    # 3. Trava de Engine Monolitica
    root.mainloop()


if __name__ == "__main__":
    main()
