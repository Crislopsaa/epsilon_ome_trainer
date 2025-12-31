"""
ES: Este script define una función que convierte un string con código LaTeX en un PDF.\n
EN: This script defines a function that turns a string with LaTeX code into a PDF.
"""


import subprocess
import tempfile
import shutil
import pathlib


def latex2pdf(latex_code: str, output_path: pathlib.Path, motor: str = "pdflatex") -> None:
    """
    ES: Convierte un string con código LaTeX en un PDF.\n
    EN: Turns a string with LaTeX code into a PDF.
    
    Warning:
        ES: La ruta del compilador elegido debe estar en el PATH de Windows (o equivalente).
        EN: The chosen compiler's path must be in the Windows PATH (or equivalent).
    
    :param latex_code: String that contains the LaTeX code to compile.
    :type latex_code: str
    :param output_path: Absolute path to where the final PDF will be located.
    :type output_path: Path
    :param motor: Compilation engine. Optional: pdflatex by default.
    :type motor: str
    """
    
    # creando un directorio temporal para compilar
    # creating a temporary directory for compilation
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = pathlib.Path(tmpdir_str)

        tex_filename = pathlib.Path("problem_data.tex")
        pdf_filename = pathlib.Path("problem_data.pdf")
        
        tex_file_path = tmpdir / tex_filename

        with open(tex_file_path, "w", encoding="utf-8") as f:
            f.write(latex_code)

        # compilando a un PDF temporal usando el motor dado (pdflatex por defecto)
        # compiling a temporary PDF using the given engine (pdflatex by default)
        try:
            subprocess.run(
                [motor, "-no-shell-escape", "-interaction=nonstopmode", str(tex_filename)],
                cwd=tmpdir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
            temporary_pdf_path = tmpdir / pdf_filename
            
            if temporary_pdf_path.exists():
                shutil.copy(temporary_pdf_path, output_path)
            
            else:
                raise RuntimeError("El proceso terminó pero no se generó el archivo PDF.")
            
            
        # recogiendo las excepciones posibles
        # handling possible exceptions
        except FileNotFoundError:
            raise RuntimeError(f"No se encontró el motor '{motor}'. Asegúrese de tener pdflatex (o el motor elegido) instalado y con la ruta añadida al PATH de Windows o equivalente (aunque al instalar Epsilon OME Trainer se le debería haber descargado ya pdflatex).")
        
        except subprocess.CalledProcessError:
            raise RuntimeError("Me temo que ha ocurrido un error al compilar el código LaTeX. Parece que el problema estaba defectuoso, inténtelo de nuevo.")
        
        except Exception as e:
            raise RuntimeError(f"Lo siento, me temo que ha ocurrido un error a la hora de compilar el código LaTeX en PDF:\n{e}")