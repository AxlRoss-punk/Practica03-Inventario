"""Captura exclusivamente la ventana de la aplicación mediante PrintWindow (Windows)."""

import ctypes
import struct
import sys
import zlib
from ctypes import wintypes


def guardar_ventana_png(ventana, destino):
    if sys.platform != "win32":
        raise RuntimeError("La captura automática de ventanas requiere Windows.")
    ventana.update()
    usuario = ctypes.WinDLL("user32", use_last_error=True)
    gdi = ctypes.WinDLL("gdi32", use_last_error=True)
    usuario.GetAncestor.argtypes = [wintypes.HWND, wintypes.UINT]
    usuario.GetAncestor.restype = wintypes.HWND
    usuario.GetClientRect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
    usuario.GetDC.argtypes = [wintypes.HWND]
    usuario.GetDC.restype = wintypes.HDC
    usuario.ReleaseDC.argtypes = [wintypes.HWND, wintypes.HDC]
    usuario.PrintWindow.argtypes = [wintypes.HWND, wintypes.HDC, wintypes.UINT]
    gdi.CreateCompatibleDC.argtypes = [wintypes.HDC]
    gdi.CreateCompatibleDC.restype = wintypes.HDC
    gdi.CreateDIBSection.argtypes = [wintypes.HDC, ctypes.c_void_p, wintypes.UINT, ctypes.POINTER(ctypes.c_void_p), wintypes.HANDLE, wintypes.DWORD]
    gdi.CreateDIBSection.restype = wintypes.HBITMAP
    gdi.SelectObject.argtypes = [wintypes.HDC, wintypes.HANDLE]
    gdi.SelectObject.restype = wintypes.HANDLE
    gdi.DeleteObject.argtypes = [wintypes.HANDLE]
    gdi.DeleteDC.argtypes = [wintypes.HDC]

    identificador = usuario.GetAncestor(ventana.winfo_id(), 2)
    rectangulo = wintypes.RECT()
    if not usuario.GetClientRect(identificador, ctypes.byref(rectangulo)):
        raise ctypes.WinError(ctypes.get_last_error())
    ancho, alto = rectangulo.right, rectangulo.bottom
    dc_ventana = usuario.GetDC(identificador)
    dc_memoria = gdi.CreateCompatibleDC(dc_ventana)
    informacion = ctypes.create_string_buffer(struct.pack("<IiiHHIIiiII", 40, ancho, -alto, 1, 32, 0, 0, 0, 0, 0, 0))
    pixeles = ctypes.c_void_p()
    bitmap = gdi.CreateDIBSection(dc_ventana, informacion, 0, ctypes.byref(pixeles), None, 0)
    anterior = gdi.SelectObject(dc_memoria, bitmap)
    try:
        if not bitmap or not pixeles.value:
            raise RuntimeError("No se pudo crear el bitmap de la captura.")
        if not usuario.PrintWindow(identificador, dc_memoria, 3):
            raise RuntimeError("Windows no pudo capturar la ventana de inventario.")
        bgra = ctypes.string_at(pixeles, ancho * alto * 4)
        rgb = bytearray(ancho * alto * 3)
        rgb[0::3], rgb[1::3], rgb[2::3] = bgra[2::4], bgra[1::4], bgra[0::4]

        def bloque(nombre, datos):
            return struct.pack(">I", len(datos)) + nombre + datos + struct.pack(">I", zlib.crc32(nombre + datos) & 0xFFFFFFFF)

        filas = b"".join(b"\x00" + rgb[fila * ancho * 3:(fila + 1) * ancho * 3] for fila in range(alto))
        png = b"\x89PNG\r\n\x1a\n" + bloque(b"IHDR", struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0))
        png += bloque(b"IDAT", zlib.compress(filas)) + bloque(b"IEND", b"")
        destino.write_bytes(png)
    finally:
        gdi.SelectObject(dc_memoria, anterior)
        gdi.DeleteObject(bitmap)
        gdi.DeleteDC(dc_memoria)
        usuario.ReleaseDC(identificador, dc_ventana)

