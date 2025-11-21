from datetime import datetime

from App.models import Shift, Schedule
from App.database import db
from App.controllers.user import get_user


def _ensure_admin(admin_id):
    """
    Internal helper: load user and ensure they are an admin.
    """
    try:
        admin_id = int(admin_id)
    except (TypeError, ValueError):
        raise PermissionError("Invalid admin id")

    admin = get_user(admin_id)
    if not admin or admin.role != "admin":
        raise PermissionError("Only admins can perform this action")
    return admin


def create_schedule(admin_id, scheduleName):
    """
    UML: Admin.scheduleShift() – creating a Schedule object.
    Called by /createSchedule in AdminViews.py
    """
    _ensure_admin(admin_id)

    if not scheduleName or not scheduleName.strip():
        raise ValueError("Schedule name is required")

    new_schedule = Schedule(
        created_by=int(admin_id),
        name=scheduleName.strip(),
        created_at=datetime.utcnow()
    )

    db.session.add(new_schedule)
    db.session.commit()

    return new_schedule


def schedule_shift(admin_id, staff_id, schedule_id, start_time, end_time):
    """
    UML: Admin.scheduleShift() – assign a shift to a staff member.
    Called by /createShift in AdminViews.py
    """
    _ensure_admin(admin_id)

    # Cast IDs safely; JWT identity is a string
    try:
        staff_id = int(staff_id)
        schedule_id = int(schedule_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid staff or schedule id")

    staff = get_user(staff_id)
    if not staff or staff.role != "staff":
        raise ValueError("Invalid staff member")

    schedule = db.session.get(Schedule, schedule_id)
    if not schedule:
        raise ValueError("Invalid schedule ID")

    if start_time >= end_time:
        raise ValueError("Shift start time must be before end time")

    new_shift = Shift(
        staff_id=staff_id,
        schedule_id=schedule_id,
        start_time=start_time,
        end_time=end_time
    )

    db.session.add(new_shift)
    db.session.commit()

    return new_shift


def get_shift_report(admin_id):
    """
    UML: Admin.viewShift() – get a list of all shifts (report).
    Called by /shiftReport in AdminViews.py
    """
    _ensure_admin(admin_id)

    # For now: simple report (can be grouped by staff/schedule later)
    shifts = Shift.query.order_by(Shift.start_time).all()
    return [shift.get_json() for shift in shifts]
