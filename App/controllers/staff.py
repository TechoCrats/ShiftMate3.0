from App.models import Shift
from App.database import db
from datetime import datetime
from App.controllers.user import get_user

def get_combined_roster(staff_id):
    staff = get_user(staff_id)
    if not staff or staff.role != "staff":
        raise PermissionError("Only staff can view roster")
    return [shift.get_json() for shift in Shift.query.order_by(Shift.start_time).all()]

def clock_in(staff_id, shift_id):
    staff = get_user(staff_id)
    if not staff or staff.role != "staff":
        raise PermissionError("Only staff can clock in")
    
    shift = Shift.query.filter_by(id=shift_id, staff_id=staff_id).first()
    if not shift:
        raise ValueError("Invalid shift for staff")
    
    if shift.clock_in:
        raise ValueError("Already clocked in")
    
    shift.clock_in = datetime.now()
    db.session.commit()
    return shift

def clock_out(staff_id, shift_id):
    staff = get_user(staff_id)
    if not staff or staff.role != "staff":
        raise PermissionError("Only staff can clock out")
    
    shift = Shift.query.filter_by(id=shift_id, staff_id=staff_id).first()
    if not shift:
        raise ValueError("Invalid shift for staff")
    
    if shift.clock_out:
        raise ValueError("Already clocked out")
    
    shift.clock_out = datetime.now()
    db.session.commit()
    return shift

def get_shift(shift_id):
    return Shift.query.get(shift_id)