import logging
import warnings
from datetime import datetime

class Plogger():

    DATE_FMT = '%Y-%m-%d %h:%M:%S'

    
    def __init__(self, name: str, log_file: str, level=logging.INFO):
        '''
        Cria uma instância que é capaz de logar para o stdout e para um arquivo.

        Parameters:
        name     (´str´)          : Nome do logger.
        log_file (´str´)          : Path para o arquivo de que armazenará os logs.
        level    (´logging.level´): Nível de saída dos logs.
        '''
        self._level = level
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
        '%d/%m/%Y %I:%M:%S %p')
                            
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)

        self._logger = logging.getLogger(name)
        if self._logger.hasHandlers():
            self._logger.handlers.clear()

        self._logger.setLevel(level)    
        self._logger.addHandler(handler)


    @property
    def str_utf_now(self):
        return datetime.utcnow().strftime(self.DATE_FMT)

    def _print(self, msg, level):
        if getattr(logging, level) >= self._level:
            print(f'{self.str_utf_now};{level};{msg}')

    def info(self, msg, *args, **kwargs):
        
        self._print(msg, 'INFO')
        self._logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        
        warnings.warn("The 'warn' method is deprecated, "
            "use 'warning' instead", DeprecationWarning, 2)
        self._print(msg, 'WARN')
        self._logger.warn(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        
        self._print(msg, 'WARN')
        self._logger.warning(msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        
        self._print(msg, 'DEBUG')
        self._logger.debug(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        
        self._print(msg, 'ERROR')
        self._logger.error(msg, *args, **kwargs)

if __name__ == '__main__':
    plogger = Plogger('test1', 'test1.log')
    plogger2 = Plogger('test2', 'test2.log')
    
    plogger.info("Teste Info")
    plogger2.info("Teste2 Info")

    plogger.debug("Teste Debug")
    plogger2.debug("Teste2 Debug")

    plogger.warning("Teste Warning")
    plogger2.warning("Teste2 Warning")

    plogger.error("Teste Error")
    plogger2.error("Teste2 Error")