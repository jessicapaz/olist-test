from .models import Price


class Bill:
    def __init__(self, call_start):
        self.call_start = call_start

    def _get_tarrif_type(self):
        hour = self.call_start.timestamp.hour
        if 6 <= hour < 22:
            return Price.objects.filter(tarrif_type='standard').last()
        elif hour >= 22 or hour < 6:
            return Price.objects.filter(tarrif_type='reduced').last()

    def calculate_price(self, duration):
        minutes = int(duration.total_seconds()/60)
        tarrif = self._get_tarrif_type()
        call_charge = float(tarrif.call_charge)
        standing_charge = float(tarrif.standing_charge)
        price = call_charge * minutes + standing_charge
        return price
