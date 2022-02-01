from typing import Optional, Dict, Any

from .abstract import DataSourceAbstract


class DataSourceRabbitMQ(DataSourceAbstract):
    def __init__(self):
        # connect to rabbit
        pass

    def get_data(self) -> Optional[Dict[Any, Any]]:
        # get data from rabbit and return json
        pass
