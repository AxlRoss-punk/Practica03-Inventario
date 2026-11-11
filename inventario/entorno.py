"""Compatibilidad local con instalaciones de Python que omiten los scripts Tcl/Tk."""

import os
import tkinter as tk
from pathlib import Path


def crear_ventana():
    try:
        return tk.Tk()
    except tk.TclError as exc:
        if "init.tcl" not in str(exc):
            raise
        import _tkinter

        runtime = Path(__file__).resolve().parent.parent / ".runtime"
        tcl = runtime / f"tcl{_tkinter.TCL_VERSION}"
        motor_tk = runtime / f"tk{_tkinter.TK_VERSION}"
        if not (tcl / "init.tcl").is_file() or not (motor_tk / "tk.tcl").is_file():
            raise
        os.environ["TCL_LIBRARY"] = str(tcl)
        os.environ["TK_LIBRARY"] = str(motor_tk)
        return tk.Tk()

