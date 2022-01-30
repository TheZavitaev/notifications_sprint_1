from abc import abstractmethod, ABC


class EmailSenderAbstract(ABC):
    @abstractmethod
    def send(self, address: str, subject: str, data: str):
        pass
