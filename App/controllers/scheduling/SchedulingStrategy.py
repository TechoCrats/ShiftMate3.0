from abc import ABC, abstractmethod
from datetime import datetime

class SchedulingStrategy(ABC):  # abstract class for scheduling strategies
    
    @abstractmethod
    def generate_schedule(self, staff, shifts, start_date, end_date):
        pass
    
    def _reset_assignments(self, staff, shifts):
        for person in staff:
            if hasattr(person, 'assigned_shifts'):
                person.assigned_shifts = []
            if hasattr(person, 'total_hours'):
                person.total_hours = 0
            if hasattr(person, 'days_worked'):
                person.days_worked = 0
                
        for shift in shifts:
            if hasattr(shift, 'assigned_staff'):
                shift.assigned_staff = []
    
    def _format_schedule(self, shifts):
        formatted = {}
        for shift in shifts:
            if hasattr(shift, 'start_time'):
                date_str = shift.start_time.strftime("%Y-%m-%d")
            else:
                continue
                
            if date_str not in formatted:
                formatted[date_str] = []
                
            shift_info = {
                "shift_id": getattr(shift, 'id', 'unknown'),
                "start_time": getattr(shift, 'start_time', 'unknown'),
                "end_time": getattr(shift, 'end_time', 'unknown'),
            }
            
            if hasattr(shift, 'assigned_staff'):
                shift_info["staff"] = [getattr(staff, 'username', 'unknown') for staff in shift.assigned_staff]
            else:
                shift_info["staff"] = []
                
            formatted[date_str].append(shift_info)
        return formatted
    
    def _generate_summary(self, staff):
        if not staff:
            return {
                "total_staff": 0,
                "total_hours_assigned": 0,
                "average_hours_per_staff": 0,
                "min_hours": 0,
                "max_hours": 0,
                "total_shifts_assigned": 0
            }
            
        total_hours = sum(getattr(person, 'total_hours', 0) for person in staff)
        total_staff = len(staff)
        
        hours_list = [getattr(person, 'total_hours', 0) for person in staff]
        shifts_list = [len(getattr(person, 'assigned_shifts', [])) for person in staff]
        
        return {
            "total_staff": total_staff,
            "total_hours_assigned": total_hours,
            "average_hours_per_staff": total_hours / total_staff if total_staff > 0 else 0,
            "min_hours": min(hours_list) if hours_list else 0,
            "max_hours": max(hours_list) if hours_list else 0,
            "total_shifts_assigned": sum(shifts_list)
        }