from .models import Price


class Bill:
    def __init__(self, call_start):
        self.call_start = call_start
    
    def _get_tarrif_type(self):
        hour = self.call_start.timestamp.hour
        if 6 <= hour < 22:
            return Price.objects.filter(tarrif_type='standard').last()
        elif 22 >= hour < 6:
            return  Price.objects.filter(tarrif_type='reduced').last()
    
    def calculate_price(self, duration):
        minutes = int(duration.total_seconds()/60)
        tarrif = self._get_tarrif_type()
        price = float(tarrif.call_charge) * minutes + float(tarrif.standing_charge)
        return price
        
    