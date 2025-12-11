#!/usr/bin/env python3
"""Lanzador DFIR de herramientas open source para sistemas Debian/Kali."""

import argparse
import os
import shutil
import subprocess
import sys
from typing import Dict, Optional, Tuple

TOOLS: Dict[str, Dict[str, str]] = {
    "1": {
        "name": "exiftool",
        "package": "libimage-exiftool-perl",
        "description": "Muestra y analiza metadatos EXIF, IPTC y XMP de imágenes y otros archivos.",
    },
    "2": {
        "name": "file",
        "package": "file",
        "description": "Detecta el tipo real de archivo mediante firmas (magic numbers).",
    },
    "3": {
        "name": "strings",
        "package": "binutils",
        "description": "Extrae cadenas imprimibles desde archivos binarios.",
    },
    "4": {
        "name": "xxd",
        "package": "xxd",
        "description": "Genera un volcado hexadecimal (hexdump) del archivo.",
    },
    "5": {
        "name": "binwalk",
        "package": "binwalk",
        "description": "Analiza archivos en busca de firmas, secciones, compresión y datos embebidos.",
    },
    "6": {
        "name": "bulk_extractor",
        "package": "bulk-extractor",
        "description": "Extrae artefactos forenses como URLs, correos o patrones desde datos crudos.",
    },
    "7": {
        "name": "pdfinfo",
        "package": "poppler-utils",
        "description": "Muestra metadatos e información estructural de documentos PDF.",
    },
    "8": {
        "name": "identify",
        "package": "imagemagick",
        "description": "Muestra información de imágenes, formatos, dimensiones y perfiles.",
    },
}


def _is_debian_based() -> bool:
    """Detecta si el sistema es Debian o derivado."""
    os_release = "/etc/os-release"
    if not os.path.exists(os_release):
        return False
    try:
        with open(os_release, "r", encoding="utf-8") as f:
            content = f.read().lower()
    except OSError:
        return False
    for token in ("debian", "ubuntu", "kali"):
        if token in content:
            return True
    return False


def check_and_install_tools() -> None:
    """Verifica la presencia de herramientas y las instala si faltan."""
    debian_like = _is_debian_based()
    if not debian_like:
        print(
            "Aviso: no se detectó un sistema basado en Debian. No se intentará instalar paquetes."
        )
    updated = False
    for tool_id, tool in TOOLS.items():
        executable = tool["name"]
        if shutil.which(executable):
            continue
        print(f"La herramienta '{executable}' no está instalada.")
        if not debian_like:
            continue
        try:
            if not updated:
                print("Ejecutando 'sudo apt-get update'...")
                subprocess.run(
                    ["sudo", "apt-get", "update"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                updated = True
            print(f"Instalando paquete '{tool['package']}'...")
            subprocess.run(
                ["sudo", "apt-get", "install", "-y", tool["package"]],
                check=True,
            )
        except subprocess.CalledProcessError as exc:
            print(
                f"Error al instalar '{tool['package']}'. Código de retorno: {exc.returncode}."
            )
        except OSError as exc:
            print(f"No se pudo ejecutar el gestor de paquetes: {exc}.")


def print_tools_list() -> None:
    """Muestra la lista de herramientas disponibles."""
    print("Herramientas disponibles:")
    for tool_id, tool in sorted(TOOLS.items(), key=lambda item: int(item[0])):
        print(f"  {tool_id}. {tool['name']} - {tool['description']}")


def resolve_tool(selection: str) -> Optional[Tuple[str, Dict[str, str]]]:
    """Resuelve la selección a un registro de herramienta."""
    if not selection:
        return None
    selection_lower = selection.lower()
    if selection in TOOLS:
        tool = TOOLS[selection]
        return selection, tool
    for tool_id, tool in TOOLS.items():
        if tool["name"].lower() == selection_lower:
            return tool_id, tool
    return None


def run_tool(tool: Dict[str, str], arguments: list[str], output_path: Optional[str]) -> int:
    """Ejecuta la herramienta con argumentos y maneja la salida."""
    cmd = [tool["name"]] + arguments
    print(f"Ejecutando: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        print("La herramienta no está instalada o no se encuentra en el PATH.")
        return 1
    except OSError as exc:
        print(f"No se pudo ejecutar la herramienta: {exc}.")
        return 1

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("[stderr]")
        print(result.stderr)

    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result.stdout)
            print(f"Salida guardada en: {output_path}")
        except OSError as exc:
            print(f"No se pudo guardar la salida en el archivo: {exc}.")

    if result.returncode != 0:
        print(f"La herramienta devolvió un código de retorno {result.returncode}.")
    return result.returncode


def build_parser() -> argparse.ArgumentParser:
    epilog_lines = ["Herramientas disponibles:"]
    for tool_id, tool in sorted(TOOLS.items(), key=lambda item: int(item[0])):
        epilog_lines.append(f"  {tool_id}. {tool['name']} - {tool['description']}")
    epilog = "\n".join(epilog_lines)

    parser = argparse.ArgumentParser(
        description="Lanzador DFIR para herramientas de línea de comandos.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-l", "--lista", action="store_true", help="Listar herramientas y salir.")
    parser.add_argument(
        "-t",
        "--tool",
        help="Número o nombre de la herramienta a ejecutar.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Archivo donde guardar la salida estándar.",
    )
    parser.add_argument(
        "params",
        nargs=argparse.REMAINDER,
        help="Parámetros adicionales que se pasarán a la herramienta seleccionada.",
    )
    return parser


def main() -> None:
    if len(sys.argv) == 1:
        print(
            "Uso básico: use -l para listar herramientas o -t <herramienta> seguido de parámetros."
        )
        return

    parser = build_parser()
    args = parser.parse_args()

    check_and_install_tools()

    if args.lista:
        print_tools_list()
        return

    if not args.tool:
        print("Debe especificar una herramienta con -t o --tool. Use -l para ver opciones.")
        return

    resolved = resolve_tool(args.tool)
    if not resolved:
        print("La herramienta indicada no existe. Use -l para ver las opciones disponibles.")
        return

    _, tool = resolved
    params = args.params if args.params else []
    return_code = run_tool(tool, params, args.output)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
