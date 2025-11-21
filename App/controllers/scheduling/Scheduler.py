from typing import List, Dict, Any
from datetime import datetime
from .EvenDistributeStrategy import EvenDistributeStrategy
from .MinimizeStrategy import MinimizeDaysStrategy
from .ShiftTypeStrategy import ShiftTypeStrategy

class Scheduler:
    def __init__(self):
        self.strategies = {
            "even_distribute": EvenDistributeStrategy(),
            "minimize_days": MinimizeDaysStrategy(),
            "shift_type_optimize": ShiftTypeStrategy()
        }

    def generate_schedule(self, strategy_name, staff, shifts, start_date, end_date):
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            available = list(self.strategies.keys())
            raise ValueError(f"Unknown strategy: {strategy_name}. Available strategies: {available}")
        
        return strategy.generate_schedule(staff, shifts, start_date, end_date)

    def get_available_strategies(self):
        return list(self.strategies.keys())