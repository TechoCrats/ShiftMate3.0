from datetime import datetime
from .SchedulingStrategy import SchedulingStrategy

class ShiftTypeStrategy(SchedulingStrategy):
    
    def generate_schedule(self, staff, shifts, start_date, end_date):
        self._reset_assignments(staff, shifts)
        
        # Group shifts by type
        shifts_by_type = {}
        for shift in shifts:
            shift_type = getattr(shift, 'shift_type', 'regular')
            if shift_type not in shifts_by_type:
                shifts_by_type[shift_type] = []
            shifts_by_type[shift_type].append(shift)
        
        # Assign preferred shifts first
        for shift_type, type_shifts in shifts_by_type.items():
            for shift in type_shifts:
                needed = getattr(shift, 'required_staff', 1) - len(getattr(shift, 'assigned_staff', []))
                if needed <= 0:
                    continue
                
                # Find staff who prefer this shift type
                preferred_staff = [s for s in staff 
                                 if shift_type in getattr(s, 'preferred_shift_types', []) and
                                 self._can_work_shift(s, shift)]
                
                preferred_staff.sort(key=lambda s: self._preferred_shift_ratio(s))
                
                for person in preferred_staff[:needed]:
                    max_hours = getattr(person, 'max_hours_per_week', 40)
                    current_hours = getattr(person, 'total_hours', 0)
                    shift_hours = getattr(shift, 'duration_hours', 8)
                    
                    if (current_hours + shift_hours <= max_hours and
                        len(getattr(shift, 'assigned_staff', [])) < getattr(shift, 'required_staff', 1)):
                        self._assign_shift(person, shift)
        
        return self._create_schedule_result(staff, shifts)

    def _can_work_shift(self, staff, shift):
        if not hasattr(shift, 'start_time'):
            return False
            
        unavailable_days = getattr(staff, 'unavailable_days', [])
        required_skills = getattr(shift, 'required_skills', [])
        staff_skills = getattr(staff, 'skills', [])
        
        return (shift.start_time.weekday() not in unavailable_days and
                all(skill in staff_skills for skill in required_skills))

    def _preferred_shift_ratio(self, staff):
        assigned_shifts = getattr(staff, 'assigned_shifts', [])
        if not assigned_shifts:
            return 0.0
            
        preferred_count = sum(1 for shift in assigned_shifts 
                            if getattr(shift, 'shift_type', 'regular') in getattr(staff, 'preferred_shift_types', []))
        return preferred_count / len(assigned_shifts)

    def _assign_shift(self, staff, shift):
        if not hasattr(shift, 'assigned_staff'):
            shift.assigned_staff = []
        if not hasattr(staff, 'assigned_shifts'):
            staff.assigned_shifts = []
        if not hasattr(staff, 'total_hours'):
            staff.total_hours = 0
            
        shift.assigned_staff.append(staff)
        staff.assigned_shifts.append(shift)
        staff.total_hours += getattr(shift, 'duration_hours', 8)

    def _create_schedule_result(self, staff, shifts):
        summary = self._generate_summary(staff)
        preference_score = self._calculate_preference_score(staff)
        
        return {
            "strategy": "Shift Type Optimization",
            "schedule": self._format_schedule(shifts),
            "summary": summary,
            "preference_score": preference_score
        }

    def _calculate_preference_score(self, staff):
        if not staff:
            return 0.0
        total_score = 0
        for person in staff:
            assigned_shifts = getattr(person, 'assigned_shifts', [])
            if assigned_shifts:
                preferred_count = sum(1 for shift in assigned_shifts 
                                    if getattr(shift, 'shift_type', 'regular') in getattr(person, 'preferred_shift_types', []))
                total_score += (preferred_count / len(assigned_shifts)) * 100
        return total_score / len(staff)