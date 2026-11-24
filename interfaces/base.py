from abc import ABC, abstractmethod


class Interface(ABC):
    @abstractmethod
    def executar(self, gerenciador):
        """Inicia a interface usando o serviço de gerenciamento fornecido."""
        raise NotImplementedError
