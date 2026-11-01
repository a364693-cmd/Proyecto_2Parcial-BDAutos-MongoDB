import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import ast
from mongo_bridge import MongoBridge
from queries_catalog import get_all_queries

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BDAutos - MongoDB NoSQL Manager")
        self.root.geometry("1100x680")

        self.bridge = MongoBridge()
        self.queries = get_all_queries()
        self.current_query = self.queries[0]

        self._setup_ui()

    def _setup_ui(self):
        # Header 
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)

        ttk.Label(header_frame, text="Seleccionar Requerimiento:", font=("Helvetica", 10, "bold")).pack(side=tk.LEFT, padx=5)

        self.combo = ttk.Combobox(header_frame, values=[q.title for q in self.queries], width=58, state="readonly")
        self.combo.current(0)
        self.combo.pack(side=tk.LEFT, padx=5)
        self.combo.bind("<<ComboboxSelected>>", self.on_select_query)

        btn_run = ttk.Button(header_frame, text="► Ejecutar Consulta en Vivo", command=self.run_custom_query)
        btn_run.pack(side=tk.LEFT, padx=15)

        # Main Paned Window (Izquierda: Código | Derecha: Resultados)
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel Izquierdo (Editor Código)
        left_frame = ttk.LabelFrame(paned, text="Código PyMongo / Pipeline (Editable)", padding=10)
        paned.add(left_frame, weight=1)

        self.code_editor = scrolledtext.ScrolledText(
            left_frame, wrap=tk.WORD, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white"
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Panel Derecho (Tabla de Resultados)
        right_frame = ttk.LabelFrame(paned, text="Resultados en MongoDB", padding=10)
        paned.add(right_frame, weight=2)

        self.tree_frame = ttk.Frame(right_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Consulta inicial (Req 0)
        self.load_query(0)

    def load_query(self, index):
        self.current_query = self.queries[index]
        self.code_editor.config(state=tk.NORMAL)
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, self.current_query.code_text)
        self.code_editor.focus_set()
        self.execute_current()

    def on_select_query(self, event):
        idx = self.combo.current()
        self.load_query(idx)

    def execute_current(self):
        try:
            results = self.current_query.execute(self.bridge)
            self.render_table(results)
        except Exception as e:
            messagebox.showerror("Error en MongoDB", f"Fallo al ejecutar {self.current_query.title}:\n{e}")
        finally:
            self.code_editor.config(state=tk.NORMAL)
            self.code_editor.focus_set()

    def _parse_pipeline(self, raw_text):
        """Interpretar el texto como JSON o Python."""
        text = raw_text.strip()
        lines = [line for line in text.splitlines() if not line.strip().startswith("#")]
        clean_text = "\n".join(lines).strip()

        if "pipeline = " in clean_text:
            clean_text = clean_text.split("pipeline = ")[1].split("\nresults")[0].strip()

        try:
            res = json.loads(clean_text)
            if isinstance(res, list):
                return res
        except Exception:
            pass

        try:
            res = ast.literal_eval(clean_text)
            if isinstance(res, list):
                return res
        except Exception:
            pass

        raise ValueError("El texto no contiene una lista de etapas (pipeline) válida.")

    def _detect_collection(self, raw_text):
        """Determina automáticamente la colección de destino."""
        text_lower = raw_text.lower()
        if "collection: makers" in text_lower or "db.makers" in text_lower:
            return "makers"
        elif "collection: countries" in text_lower or "db.countries" in text_lower:
            return "countries"
        elif "collection: continents" in text_lower or "db.continents" in text_lower:
            return "continents"
        
        # Por defecto utiliza la colección asignada al requerimiento activo
        return getattr(self.current_query, 'collection', 'cars')

    def run_custom_query(self):
        """Ejecuta dinámicamente cualquier consulta en vivo (Modo Compass)."""
        raw_text = self.code_editor.get("1.0", tk.END).strip()

        try:
            pipeline = self._parse_pipeline(raw_text)
            target_collection = self._detect_collection(raw_text)
            results = self.bridge.execute_pipeline(target_collection, pipeline)
            self.render_table(results)
        except ValueError as ve:
            messagebox.showerror("Error de Formato", str(ve))
        except Exception as e:
            messagebox.showerror("Error de Ejecución MongoDB", f"La consulta falló en la colección objetivo:\n{e}")
        finally:
            # Recuperación del foco de teclado y edición tras error
            self.code_editor.config(state=tk.NORMAL)
            self.code_editor.focus_set()

    def render_table(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not data:
            self.tree["columns"] = ("Mensaje",)
            self.tree.heading("Mensaje", text="Sin Resultados")
            self.tree.insert("", tk.END, values=("La consulta finalizó pero no retornó documentos.",))
            return

        if len(data) == 1 and isinstance(data[0], dict) and list(data[0].keys())[0].startswith("Total"):
            key = list(data[0].keys())[0]
            self.tree["columns"] = (key,)
            self.tree.heading(key, text=key)
            self.tree.insert("", tk.END, values=(data[0][key],))
            return

        columns = list(data[0].keys())
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.W, width=140)

        for row in data:
            values = [row.get(c, "") for c in columns]
            self.tree.insert("", tk.END, values=values)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()