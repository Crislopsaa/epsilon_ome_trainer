"""
ES: Este script define al QObject que ejecuta funciones pesadas de forma asíncrona.

EN: This script defines the QObject that executes heavy functions asynchronously.
"""


from PyQt5.QtCore import QObject, pyqtSignal


class Worker(QObject):
    """
    ES: QObject que ejecuta funciones pesadas de forma asíncrona.
    
    EN: QObject that executes heavy functions asynchronously.
    """
    finish_signal = pyqtSignal()
    error_signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()   
    
    def run(self, process: callable):
        """
        ES: Ejecuta una función dada y envía las excepciones al hilo principal.
        
        EN: Executes a given function and sends the exceptions to the main thread.
        
        :param process: The heavy function to execute.
        :type process: callable
        """  
        try:
            process()
            self.finish_signal.emit()
            
        except Exception as e:
            self.error_signal.emit(e)