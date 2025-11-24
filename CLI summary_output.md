# Complete CLI Commands Output 


## Available Commands Summary

### Initialize
```bash
flask init
```

### User Management
```bash
flask user create <username> <password> <role>
flask user list [json]
```

### Authentication
```bash
flask auth login <username> <password>
flask auth logout <username>
```

### Schedule Management
```bash
flask schedule create <name>
flask schedule list
flask schedule view <schedule_id>
flask schedule auto <schedule_id> <strategy> [--days] [--shifts-per-day] [--shift-type]
```

### Shift Operations
```bash
flask shift schedule <staff_id> <schedule_id> <start> <end>
flask shift roster           # Staff view roster
flask shift clockin <shift_id>     # Staff clock in
flask shift clockout <shift_id>    # Staff clock out
flask shift report           # Admin view report
```

### Preferences
```bash
flask prefs set <staff_id> [--preferred "shift,types"] [--skills "skill1,skill2"] [--unavailable "0,1"] [--max_hours 40]
flask prefs get <staff_id>
```

### Testing
```bash
pytest #run all test
flask test user           # Run all user tests
flask test user unit      # Run unit tests
flask test user int       # Run integration tests
```

---

# === SHIFTMATE COMPLETE CLI WORKFLOW ===

# 1. INITIAL SETUP
echo "=== STEP 1: DATABASE SETUP ==="
python -m flask init

# 2. CREATE USERS
echo "=== STEP 2: CREATE USERS ==="
python -m flask user create admin adminpass admin
python -m flask user create jane janepass staff
python -m flask user create bobstaff bobpass staff
python -m flask user create alice alicepass staff

# 3. VERIFY USERS
echo "=== STEP 3: VERIFY USERS ==="
python -m flask user list

# 4. ADMIN LOGIN & SETUP
echo "=== STEP 4: ADMIN SETUP ==="
python -m flask auth login admin adminpass
python -m flask auth whoami

# 5. CREATE SCHEDULES
echo "=== STEP 5: CREATE SCHEDULES ==="
python -m flask schedule create "December Schedule"
python -m flask schedule create "January Schedule"

# 6. AUTO-GENERATE SHIFTS
echo "=== STEP 6: AUTO-GENERATE SHIFTS ==="
python -m flask schedule auto 1 even-distribute --days 3 --shifts-per-day 2
python -m flask schedule auto 2 preference-based --days 2 --shifts-per-day 3

# 7. VIEW SCHEDULES
echo "=== STEP 7: VIEW SCHEDULES ==="
python -m flask schedule list
python -m flask schedule view 1
python -m flask schedule view 2

# 8. SET PREFERENCES
echo "=== STEP 8: SET PREFERENCES ==="
python -m flask prefs set 2 --preferred "morning,day" --skills "cashier" --max_hours 40 --unavailable "1,3"
python -m flask prefs set 3 --preferred "evening" --skills "stocking" --max_hours 35 --unavailable "0,6"

# 9. VERIFY PREFERENCES
echo "=== STEP 9: VERIFY PREFERENCES ==="
python -m flask prefs get 2
python -m flask prefs get 3
python -m flask prefs list

# 10. MANUAL SHIFT SCHEDULING
echo "=== STEP 10: MANUAL SHIFT SCHEDULING ==="
python -m flask shift schedule 2 1 "2024-12-25 09:00:00" "2024-12-25 17:00:00"
python -m flask shift schedule 3 1 "2024-12-26 14:00:00" "2024-12-26 22:00:00"

# 11. VIEW UPDATED SCHEDULE
echo "=== STEP 11: VIEW UPDATED SCHEDULE ==="
python -m flask schedule view 1

# 12. ADMIN REPORT
echo "=== STEP 12: ADMIN REPORT ==="
python -m flask shift report

# 13. LOGOUT ADMIN
echo "=== STEP 13: LOGOUT ADMIN ==="
python -m flask auth logout

# 14. STAFF OPERATIONS
echo "=== STEP 14: STAFF OPERATIONS ==="

# Jane's operations
python -m flask auth login jane janepass
python -m flask auth whoami
python -m flask shift roster
python -m flask shift clockin 1
python -m flask shift clockout 1
python -m flask shift roster
python -m flask auth logout

# Bobstaff's operations
python -m flask auth login bobstaff bobpass
python -m flask auth whoami
python -m flask shift roster
python -m flask shift clockin 3
python -m flask shift clockout 3
python -m flask shift roster
python -m flask auth logout

# Alice's operations
python -m flask auth login alice alicepass
python -m flask auth whoami
python -m flask shift roster
python -m flask shift clockin 2
python -m flask shift clockout 2
python -m flask shift roster
python -m flask auth logout

# 15. FINAL ADMIN CHECK
echo "=== STEP 15: FINAL ADMIN CHECK ==="
python -m flask auth login admin adminpass
python -m flask shift report
python -m flask schedule view 1
python -m flask schedule view 2
python -m flask user list
python -m flask prefs get 2
python -m flask prefs get 3
python -m flask prefs list

# 16. FINAL LOGOUT
echo "=== STEP 16: FINAL LOGOUT ==="
python -m flask auth logout

