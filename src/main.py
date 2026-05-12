import tkinter as tk
from controllers import ControladorDoJogo
from views import TkinterView

def main():
    """Entrypoint de Bootstraping do Padrão MVC para Inicialização Unida."""
    # 1. Spawn Application Core
    root = tk.Tk()
    
    # 2. Injeta as Dependências na Via Crítica
    controlador = ControladorDoJogo()
    aplicativo = TkinterView(root, controlador)
    
    # 3. Trava de Engine Monolítica
    root.mainloop()

if __name__ == "__main__":
    main()
