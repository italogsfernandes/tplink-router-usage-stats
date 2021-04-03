from contants import PRECO_POR_GB
from config import get_apelidos_mac

APELIDOS_MAC = get_apelidos_mac()


class StatDataMixin:
    @property
    def total_kb(self):
        return self.total_byte / 1024.0

    @property
    def total_mb(self):
        return self.total_kb / 1024.0

    @property
    def total_gb(self):
        return self.total_mb / 1024.0

    @property
    def total_preco(self):
        return self.get_total_preco(self.total_byte)

    def get_total_preco(self, total_byte):
        total_kb = total_byte / 1024.0
        total_mb = total_kb / 1024.0
        total_gb = total_mb / 1024.0
        return total_gb * PRECO_POR_GB

    @property
    def apelido(self):
        try:
            return APELIDOS_MAC[self.mac.upper()]
        except KeyError:
            return f"Desconhecido ({self.mac.upper()})"

    @property
    def total_best_unit(self):
        return self.get_total_best_unit(self.total_byte)

    def get_total_best_unit(self, total_byte):
        total_kb = total_byte / 1024.0
        total_mb = total_kb / 1024.0
        total_gb = total_mb / 1024.0
        if total_byte < 1024:
            return f"{total_byte:.2f} B"
        elif total_kb < 1024:
            return f"{total_kb:.2f} KB"
        elif total_mb < 1024:
            return f"{total_mb:.2f} MB"
        else:
            return f"{total_gb:.2f} GB"

    def __str__(self):
        return f"{self.apelido}: {self.total_best_unit} --> R${self.total_preco:.2f}"
