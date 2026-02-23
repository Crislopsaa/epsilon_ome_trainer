"""
ES: Este script define al QObject que ejecuta funciones pesadas de forma asíncrona.

EN: This script defines the QObject that executes heavy functions asynchronously.
"""


from typing_extensions import Iterable

from PyQt5.QtCore import QObject, pyqtSignal


class Worker(QObject):
    """
    ES: QObject que ejecuta funciones pesadas de forma asíncrona.
    
    EN: QObject that executes heavy functions asynchronously.
    """
    progress_signal = pyqtSignal(int)
    finish_signal = pyqtSignal()
    error_signal = pyqtSignal(object)
    
    def __init__(self, function_to_run: callable = None, args: Iterable = None):
        super().__init__()
        self.function_to_run = function_to_run
        self.args = args 
    
    def run(self) -> None:
        """
        ES: Ejecuta una función dada y envía las excepciones al hilo principal.
        
        EN: Executes a given function and sends the exceptions to the main thread.
        
        Warning:
            ES: La función a ejecutar y sus argumentos deben haber sido previamente establecidos como atributos de la clase. Si no, se lanzará un TypeError.
            
            EN: The function to execute and its arguments must have been previously loaded as attributes of the class; else, a TypeError will be thrown.
        """  
        try:
            if self.function_to_run is None:
                raise TypeError("[worker.py] ERROR: Se ha intentado correr una función en el Worker sin especificarla.")
                
            elif self.args is not None:
                self.function_to_run(*self.args)   
                
            else:
                self.function_to_run()      
            
            self.finish_signal.emit()
            
        except Exception as e:
            self.error_signal.emit(e)