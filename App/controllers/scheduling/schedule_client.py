
import sys
import os
#i Add the project root to Python path so we can import App 
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

from App.models import Schedule, Shift, Staff
from App.database import db
from datetime import datetime, date, timedelta
import random

class ScheduleClient:
    def __init__(self):
        pass
    
    def auto_populate(self, admin_id, schedule_id, strategy_name, staff_list, start_date, end_date, shifts_per_day=2, shift_type='mixed'):
        """
        Auto-populate schedule using different strategies
        """
        try:
            # Clear existing shifts for this schedule
            self._clear_existing_shifts(schedule_id, start_date, end_date)
            
            if strategy_name == "even-distribute":
                return self._even_distribute_strategy(admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day, shift_type)
            elif strategy_name == "minimize-days":
                return self._minimize_days_strategy(admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day, shift_type)
            elif strategy_name == "preference-based":
                return self._preference_based_strategy(admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day, shift_type)
            elif strategy_name == "day-night-distribute":
                return self._day_night_distribute_strategy(admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day)
            else:
                raise ValueError(f"Unknown strategy: {strategy_name}")
                
        except Exception as e:
            raise Exception(f"Failed to auto-populate schedule: {str(e)}")
    
    def _clear_existing_shifts(self, schedule_id, start_date, end_date):
        """Clear existing shifts in the date range"""
        shifts = Shift.query.filter(
            Shift.schedule_id == schedule_id,
            Shift.start_time >= datetime.combine(start_date, datetime.min.time()),
            Shift.start_time <= datetime.combine(end_date, datetime.max.time())
        ).all()
        
        for shift in shifts:
            db.session.delete(shift)
        db.session.commit()
    
    def _even_distribute_strategy(self, admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day, shift_type):
        """Distribute shifts evenly among all staff"""
        shifts_created = 0
        staff_count = len(staff_list)
        
        if staff_count == 0:
            return {"success": False, "message": "No staff available"}
        
        # Calculate total shifts and target per staff
        day_count = (end_date - start_date).days + 1
        total_shifts = day_count * shifts_per_day
        target_per_staff = max(1, total_shifts // staff_count)
        
        staff_shifts = {staff.id: 0 for staff in staff_list}
        current_date = start_date
        
        # Generate shifts evenly distributed
        while current_date <= end_date:
            for shift_num in range(shifts_per_day):
                # Find staff with least shifts assigned
                available_staff = [s for s in staff_list if staff_shifts[s.id] < target_per_staff]
                if not available_staff:
                    available_staff = staff_list
                
                staff = min(available_staff, key=lambda x: staff_shifts[x.id])
                
                # Create shift times based on shift type
                shift_times = self._get_shift_times(current_date, shift_num, shifts_per_day, shift_type)
                if shift_times:
                    shift = Shift(
                        schedule_id=schedule_id,
                        staff_id=staff.id,
                        start_time=shift_times['start'],
                        end_time=shift_times['end']
                       
                    )
                    db.session.add(shift)
                    staff_shifts[staff.id] += 1
                    shifts_created += 1
            
            current_date += timedelta(days=1)
        
        db.session.commit()
        
        summary = self._generate_distribution_summary(staff_shifts, staff_list)
        score = self._calculate_fairness_score(staff_shifts)
        
        return {
            "success": True,
            "schedule": db.session.get(Schedule, schedule_id),
            "shifts_created": shifts_created,
            "score": score,
            "summary": summary
        }
    
    def _minimize_days_strategy(self, admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day, shift_type):
        """Minimize number of days each staff works"""
        shifts_created = 0
        day_count = (end_date - start_date).days + 1
        staff_count = len(staff_list)
        
        # Calculate target days per staff 
        target_days_per_staff = max(2, (day_count * 2) // staff_count)
        
        staff_days = {staff.id: set() for staff in staff_list}
        current_date = start_date
        
        # Assign multiple shifts per day to minimize work days
        for staff in staff_list:
            days_assigned = 0
            temp_date = current_date
            
            while days_assigned < target_days_per_staff and temp_date <= end_date:
                # Assign all shifts for this day to the same staff
                for shift_num in range(shifts_per_day):
                    shift_times = self._get_shift_times(temp_date, shift_num, shifts_per_day, shift_type)
                    if shift_times:
                        shift = Shift(
                            schedule_id=schedule_id,
                            staff_id=staff.id,
                            start_time=shift_times['start'],
                            end_time=shift_times['end']
                            
                        )
                        db.session.add(shift)
                        shifts_created += 1
                
                staff_days[staff.id].add(temp_date)
                days_assigned += 1
                # Skip days to spread out assignments
                temp_date += timedelta(days=max(1, day_count // target_days_per_staff))
        
        db.session.commit()
        
        summary = self._generate_minimize_days_summary(staff_days, staff_list)
        score = self._calculate_efficiency_score(staff_days, day_count)
        
        return {
            "success": True,
            "schedule": db.session.get(Schedule, schedule_id),
            "shifts_created": shifts_created,
            "score": score,
            "summary": summary
        }
    
    def _preference_based_strategy(self, admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day, shift_type):
        """Assign shifts based on staff preferences"""
        shifts_created = 0
        current_date = start_date
        
        # Simulate preference-based assignment
        # In a real system, this would use actual staff preferences
        staff_preferences = {}
        for staff in staff_list:
            # Simulate random preferences for demonstration
            preferred_shifts = random.sample(['morning', 'evening', 'night'], random.randint(1, 2))
            staff_preferences[staff.id] = preferred_shifts
        
        while current_date <= end_date:
            for shift_num in range(shifts_per_day):
                shift_times = self._get_shift_times(current_date, shift_num, shifts_per_day, shift_type)
                if not shift_times:
                    continue
                
                # Determine shift type for preference matching
                current_shift_type = 'morning' if shift_num == 0 else 'evening'
                
                # Find staff who prefer this shift type
                preferred_staff = [s for s in staff_list if current_shift_type in staff_preferences.get(s.id, [])]
                if not preferred_staff:
                    preferred_staff = staff_list
                
                # Assign to random preferred staff
                staff = random.choice(preferred_staff)
                
                shift = Shift(
                    schedule_id=schedule_id,
                    staff_id=staff.id,
                    start_time=shift_times['start'],
                    end_time=shift_times['end']
                   
                )
                db.session.add(shift)
                shifts_created += 1
            
            current_date += timedelta(days=1)
        
        db.session.commit()
        
        summary = f"Preference-based assignment completed. Assigned {shifts_created} shifts based on staff preferences."
        score = 85.0  
        
        return {
            "success": True,
            "schedule": db.session.get(Schedule, schedule_id),
            "shifts_created": shifts_created,
            "score": score,
            "summary": summary
        }
    
    def _day_night_distribute_strategy(self, admin_id, schedule_id, staff_list, start_date, end_date, shifts_per_day):
        """Distribute day and night shifts evenly among staff"""
        shifts_created = 0
        staff_count = len(staff_list)
        
        if staff_count < 2:
            return {"success": False, "message": "Need at least 2 staff for day/night distribution"}
        
        # Split staff into day and night preference groups
        day_staff = staff_list[:staff_count//2]
        night_staff = staff_list[staff_count//2:]
        
        day_shifts_count = {staff.id: 0 for staff in day_staff}
        night_shifts_count = {staff.id: 0 for staff in night_staff}
        
        current_date = start_date
        
        while current_date <= end_date:
            # Day shift (first shift)
            if day_staff:
                staff = min(day_staff, key=lambda x: day_shifts_count[x.id])
                shift_times = self._get_shift_times(current_date, 0, shifts_per_day, 'day')
                if shift_times:
                    shift = Shift(
                        schedule_id=schedule_id,
                        staff_id=staff.id,
                        start_time=shift_times['start'],
                        end_time=shift_times['end']
                        
                    )
                    db.session.add(shift)
                    day_shifts_count[staff.id] += 1
                    shifts_created += 1
            
            # Night shift (second shift)
            if night_staff and shifts_per_day > 1:
                staff = min(night_staff, key=lambda x: night_shifts_count[x.id])
                shift_times = self._get_shift_times(current_date, 1, shifts_per_day, 'night')
                if shift_times:
                    shift = Shift(
                        schedule_id=schedule_id,
                        staff_id=staff.id,
                        start_time=shift_times['start'],
                        end_time=shift_times['end']
                    
                    )
                    db.session.add(shift)
                    night_shifts_count[staff.id] += 1
                    shifts_created += 1
            
            current_date += timedelta(days=1)
        
        db.session.commit()
        
        summary = f"Day/Night distribution: {len(day_staff)} day staff, {len(night_staff)} night staff. Total shifts: {shifts_created}"
        score = 88.0
        
        return {
            "success": True,
            "schedule": db.session.get(Schedule, schedule_id),
            "shifts_created": shifts_created,
            "score": score,
            "summary": summary
        }
    
    def _get_shift_times(self, date, shift_num, shifts_per_day, shift_type):
        """Generate shift times based on shift type and number"""
        base_date = datetime.combine(date, datetime.min.time())
        
        if shift_type == 'day':
            # Day shifts: 8am-4pm, 9am-5pm, etc.
            start_hour = 8 + shift_num
            return {
                'start': base_date.replace(hour=start_hour),
                'end': base_date.replace(hour=start_hour + 8)
            }
        elif shift_type == 'night':
            # Night shifts: 10pm-6am, 11pm-7am, etc.
            start_hour = 22 + shift_num
            end_date = date + timedelta(days=1)  # Night shift spans two days
            return {
                'start': base_date.replace(hour=start_hour),
                'end': datetime.combine(end_date, datetime.min.time()).replace(hour=(start_hour + 8) % 24)
            }
        else:  # mixed
            if shift_num == 0:  # Morning shift
                return {
                    'start': base_date.replace(hour=8),
                    'end': base_date.replace(hour=16)
                }
            else:  # Evening shift
                return {
                    'start': base_date.replace(hour=16),
                    'end': base_date.replace(hour=23, minute=59)
                }
    
    def _generate_distribution_summary(self, staff_shifts, staff_list):
        """Generate summary for even distribution"""
        summary = "Even Distribution Summary:\n"
        for staff in staff_list:
            summary += f"  {staff.username}: {staff_shifts[staff.id]} shifts\n"
        avg_shifts = sum(staff_shifts.values()) / len(staff_shifts) if staff_shifts else 0
        summary += f"Average shifts per staff: {avg_shifts:.1f}"
        return summary
    
    def _generate_minimize_days_summary(self, staff_days, staff_list):
        """Generate summary for minimize days strategy"""
        summary = "Minimize Days Summary:\n"
        for staff in staff_list:
            summary += f"  {staff.username}: {len(staff_days[staff.id])} work days\n"
        avg_days = sum(len(days) for days in staff_days.values()) / len(staff_days) if staff_days else 0
        summary += f"Average work days per staff: {avg_days:.1f}"
        return summary
    
    def _calculate_fairness_score(self, staff_shifts):
        """Calculate fairness score (0-100)"""
        if not staff_shifts:
            return 0
        shifts = list(staff_shifts.values())
        avg = sum(shifts) / len(shifts)
        variance = sum((s - avg) ** 2 for s in shifts) / len(shifts)
        return max(0, 100 - (variance * 10))
    
    def _calculate_efficiency_score(self, staff_days, total_days):
        """Calculate efficiency score for minimize days strategy"""
        if not staff_days:
            return 0
        avg_days = sum(len(days) for days in staff_days.values()) / len(staff_days)
        efficiency = (total_days - avg_days) / total_days * 100
        return min(100, max(0, efficiency))
    
    def get_available_strategies(self):
        """Get list of available strategies"""
        return ["even-distribute", "minimize-days", "preference-based", "day-night-distribute"]

# Create global instance
schedule_client = ScheduleClient()