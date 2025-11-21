from datetime import datetime
from .SchedulingStrategy import SchedulingStrategy

class MinimizeDaysStrategy(SchedulingStrategy):
    
    def generate_schedule(self, staff, shifts, start_date, end_date):
        self._reset_assignments(staff, shifts)
        
        # Group shifts by date
        shifts_by_date = {}
        for shift in shifts:
            if hasattr(shift, 'start_time'):
                date_str = shift.start_time.strftime("%Y-%m-%d") 
                if date_str not in shifts_by_date:
                    shifts_by_date[date_str] = []
                shifts_by_date[date_str].append(shift)
        
        # Assign staff to full days 
        for date_str, date_shifts in shifts_by_date.items():
            available_staff = [s for s in staff if self._is_available_on_date(s, date_shifts[0].start_time)]
            
            for shift in date_shifts:
                needed = getattr(shift, 'required_staff', 1) - len(getattr(shift, 'assigned_staff', []))
                if needed <= 0:
                    continue
                    
                candidates = [s for s in available_staff 
                            if self._can_work_shift(s, shift) and 
                            not self._has_worked_date(s, date_str)]
                
                candidates.sort(key=lambda s: getattr(s, 'days_worked', 0))
                
                for person in candidates[:needed]:
                    max_hours = getattr(person, 'max_hours_per_week', 40)
                    current_hours = getattr(person, 'total_hours', 0)
                    shift_hours = getattr(shift, 'duration_hours', 8)
                    
                    if current_hours + shift_hours <= max_hours:
                        self._assign_shift(person, shift, date_str)
                        if person in available_staff:
                            available_staff.remove(person)
        
        return self._create_schedule_result(staff, shifts)

    def _is_available_on_date(self, staff, date):
        unavailable_days = getattr(staff, 'unavailable_days', [])
        return date.weekday() not in unavailable_days

    def _can_work_shift(self, staff, shift):
        shift_type = getattr(shift, 'shift_type', 'regular')
        preferred_types = getattr(staff, 'preferred_shift_types', ['regular'])
        required_skills = getattr(shift, 'required_skills', [])
        staff_skills = getattr(staff, 'skills', [])
        
        return (shift_type in preferred_types and
                all(skill in staff_skills for skill in required_skills))

    def _has_worked_date(self, staff, date_str):
        assigned_shifts = getattr(staff, 'assigned_shifts', [])
        return any(hasattr(shift, 'start_time') and shift.start_time.strftime("%Y-%m-%d") == date_str 
                   for shift in assigned_shifts)

    def _assign_shift(self, staff, shift, date_str):
        if not hasattr(shift, 'assigned_staff'):
            shift.assigned_staff = []
        if not hasattr(staff, 'assigned_shifts'):
            staff.assigned_shifts = []
        if not hasattr(staff, 'total_hours'):
            staff.total_hours = 0
        if not hasattr(staff, 'days_worked'):
            staff.days_worked = 0
            
        shift.assigned_staff.append(staff)
        staff.assigned_shifts.append(shift)
        staff.total_hours += getattr(shift, 'duration_hours', 8)
        
        # Only count as new day if first shift of that date
        assigned_shifts = getattr(staff, 'assigned_shifts', [])
        if not any(hasattr(s, 'start_time') and s.start_time.strftime("%Y-%m-%d") == date_str 
                  for s in assigned_shifts[:-1]):
            staff.days_worked += 1

    def _create_schedule_result(self, staff, shifts):
        summary = self._generate_summary(staff)
        days_worked_list = [getattr(person, 'days_worked', 0) for person in staff]
        
        summary["average_days_per_staff"] = sum(days_worked_list) / len(staff) if staff else 0
        summary["min_days"] = min(days_worked_list) if days_worked_list else 0
        summary["max_days"] = max(days_worked_list) if days_worked_list else 0
        
        return {
            "strategy": "Minimize Days",
            "schedule": self._format_schedule(shifts),
            "summary": summary,
            "efficiency_score": self._calculate_efficiency_score(staff)
        }

    def _calculate_efficiency_score(self, staff):
        if not staff:
            return 0.0
        total_score = 0
        for person in staff:
            days_worked = getattr(person, 'days_worked', 1)
            total_hours = getattr(person, 'total_hours', 0)
            if days_worked > 0:
                avg_hours_per_day = total_hours / days_worked
                total_score += min(100, avg_hours_per_day * 10)
        return total_score / len(staff) if staff else 0.0