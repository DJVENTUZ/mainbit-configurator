import os
import subprocess
import tkinter as tk
from tkinter import messagebox


def cambiar_hostname():
  nuevo_hostname = entry_hostname.get().strip()
  if not nuevo_hostname:
    messagebox.showerror(
        "Error", "Por favor ingresa un HOSTNAME válido (ej. 513-M-L2-12345)."
    )
    return

  if messagebox.askyesno(
      "Confirmar Cambio",
      f"¿Estás seguro de cambiar el nombre del equipo a:\n'{nuevo_hostname}'?\n\nNota:"
      " Se requerirá reiniciar el equipo después.",
  ):
    try:
      cmd = f'powershell -Command "Rename-Computer -NewName \\"{nuevo_hostname}\\" -Force"'
      resultado = subprocess.run(
          cmd, shell=True, capture_output=True, text=True
      )

      if resultado.returncode == 0:
        messagebox.showinfo(
            "Éxito",
            "¡Hostname cambiado correctamente!\nEs necesario reiniciar el"
            " equipo para aplicar los cambios.",
        )
      else:
        error_msg = (
            resultado.stderr.strip()
            if resultado.stderr
            else "Error desconocido."
        )
        messagebox.showerror(
            "Error",
            f"No se pudo cambiar el hostname.\nAsegúrate de ejecutar el"
            f" programa como Administrador.\n\nDetalles: {error_msg}",
        )
    except Exception as e:
      messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")


def unir_dominio():
  dominio = "dominio.semarnat.gob.mx"
  if messagebox.askyesno(
      "Confirmar Dominio",
      f"¿Deseas unir el equipo al dominio corporativo:\n'{dominio}'?\n\nSe abrirá"
      " una ventana de comandos para ingresar tus credenciales de dominio.",
  ):
    try:
      subprocess.Popen([
          "powershell",
          "-NoExit",
          "-Command",
          f"Add-Computer -DomainName '{dominio}' -Credential (Get-Credential)",
      ])
    except Exception as e:
      messagebox.showerror("Error", f"Ocurrió un error inesperado: {str(e)}")


def abrir_sysdm():
  try:
    os.system("sysdm.cpl")
  except Exception as e:
    messagebox.showerror("Error", f"No se pudo abrir sysdm.cpl: {str(e)}")


root = tk.Tk()
root.title("Asistente de Configuración Mainbit")
root.geometry("440x420")
root.config(bg="#f0f4f8")
root.resizable(False, False)

titulo = tk.Label(
    root,
    text="Configuración de Hostname y Dominio",
    font=("Arial", 13, "bold"),
    bg="#f0f4f8",
    fg="#1e3a8a",
)
titulo.pack(pady=15)

frame_host = tk.LabelFrame(
    root,
    text=" 1. Cambio de Hostname ",
    font=("Arial", 10, "bold"),
    bg="#f0f4f8",
    fg="#333333",
    padx=12,
    pady=10,
)
frame_host.pack(fill="x", padx=20, pady=5)

lbl_inst = tk.Label(
    frame_host,
    text="Ingresa el Hostname (ej: 513-M-L2-12345):",
    bg="#f0f4f8",
    font=("Arial", 9),
    anchor="w",
)
lbl_inst.pack(fill="x", pady=2)

entry_hostname = tk.Entry(frame_host, font=("Arial", 11), width=32)
entry_hostname.pack(fill="x", pady=5)

btn_hostname = tk.Button(
    frame_host,
    text="Aplicar Nuevo Hostname",
    bg="#2563eb",
    fg="white",
    font=("Arial", 9, "bold"),
    cursor="hand2",
    command=cambiar_hostname,
)
btn_hostname.pack(fill="x", pady=5)

frame_dom = tk.LabelFrame(
    root,
    text=" 2. Unión a Dominio ",
    font=("Arial", 10, "bold"),
    bg="#f0f4f8",
    fg="#333333",
    padx=12,
    pady=10,
)
frame_dom.pack(fill="x", padx=20, pady=10)

lbl_dom = tk.Label(
    frame_dom,
    text="Dominio: dominio.semarnat.gob.mx",
    bg="#f0f4f8",
    font=("Arial", 9),
    anchor="w",
)
lbl_dom.pack(fill="x", pady=2)

btn_dominio = tk.Button(
    frame_dom,
    text="Unir a Dominio",
    bg="#16a34a",
    fg="white",
    font=("Arial", 9, "bold"),
    cursor="hand2",
    command=unir_dominio,
)
btn_dominio.pack(fill="x", pady=5)

btn_sysdm = tk.Button(
    root,
    text="Abrir Propiedades del Sistema (sysdm.cpl)",
    bg="#64748b",
    fg="white",
    font=("Arial", 9),
    cursor="hand2",
    command=abrir_sysdm,
)
btn_sysdm.pack(pady=10)

root.mainloop()
