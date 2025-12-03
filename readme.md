<h1 align= center> ShiftMate 3.0 — Flask MVC Workforce Scheduler </h1>
ShiftMate 3.0 is a lightweight Flask-based workforce rostering system for creating staff accounts, assigning shifts, tracking time, and generating simple reports. It includes automated scheduling strategies (even distribution, minimize days, and shift-type optimization) and per-staff preferences used by the scheduler.

<h2>Built With</h2>
<p align="left">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=flask,py,postman,vscode&perline=8" />
  </a>
</p>

<h3>Key features:</h3>
<li> 👥 User Management (admin & staff roles)</li>
<li>📅 Create schedules & assign shifts</li>
<li>⏱️ Clock-in / Clock-out tracking</li>
<li>📊 Attendance & shift reporting</li>
<li>🤖 Auto-generate schedules using strategies:</li>
    <ul>even-distribute</ul>
    <ul>minimize-days</ul>
    <ul>preference-based</ul>
    <ul>day-night-distribute</ul>
<li>🎯 Per-staff preferences for shift type, skills, unavailability, and weekly hours</li>
<br>

<h1>📦 Installation & Setup</h1>

## Dependencies
* Python3/pip3
* Packages listed in requirements.txt


## Installing Dependencies
```bash
$ pip install -r requirements.txt
```

## Running the Project
_For development run the server command (what you execute):_
```bash
$ flask run
```

## 📬 Postman Collection
_The Postman Collection is available here:_ <br>
https://www.postman.com/technocrats-1703/workspace/technocrats-workspace/collection/42343421-bf2fe07a-e102-4ff9-be01-c3f5e4cfa46f?action=share&creator=42343421&active-environment=33787611-86580fac-1e71-4b0a-997a-7cc6e65907d4


(CHECK TRELLO BOARD FOR CONFIGURATIONS)

## 🧪 Run the API Collection in Postman

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/42343421-bf2fe07a-e102-4ff9-be01-c3f5e4cfa46f?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D42343421-bf2fe07a-e102-4ff9-be01-c3f5e4cfa46f%26entityType%3Dcollection%26workspaceId%3Db8d276e5-e552-4175-9811-6bb3893203f9#?env%5BLocal%20Host%5D=W3sia2V5IjoiYmFzZVVybCIsInZhbHVlIjoiaHR0cHM6Ly9zaGlmdG1hdGUzLTAub25yZW5kZXIuY29tIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJodHRwczovL3NoaWZ0bWF0ZTMtMC5vbnJlbmRlci5jb20iLCJjb21wbGV0ZVNlc3Npb25WYWx1ZSI6Imh0dHBzOi8vc2hpZnRtYXRlMy0wLm9ucmVuZGVyLmNvbSIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJ0aW1lc3RhbXAiLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiIiLCJjb21wbGV0ZVNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6MX0seyJrZXkiOiJzZXNzaW9uVG9rZW4iLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiI3IiwiY29tcGxldGVTZXNzaW9uVmFsdWUiOiI3Iiwic2Vzc2lvbkluZGV4IjoyfSx7ImtleSI6InJhbmRvbVN1ZmZpeCIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4IjozfSx7ImtleSI6ImJvYiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6IiIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiIiwic2Vzc2lvbkluZGV4Ijo0fSx7ImtleSI6ImFjY2Vzc1Rva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoiIiwiY29tcGxldGVTZXNzaW9uVmFsdWUiOiIiLCJzZXNzaW9uSW5kZXgiOjV9LHsia2V5IjoiU2NoZWR1bGVfaWQiLCJ2YWx1ZSI6IjEiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6IjEiLCJjb21wbGV0ZVNlc3Npb25WYWx1ZSI6IjEiLCJzZXNzaW9uSW5kZXgiOjZ9LHsia2V5IjoiaG9zdCIsInZhbHVlIjoiaHR0cHM6Ly9zaGlmdG1hdGUzLTAub25yZW5kZXIuY29tIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJodHRwczovL3NoaWZ0bWF0ZTMtMC5vbnJlbmRlci5jb20iLCJjb21wbGV0ZVNlc3Npb25WYWx1ZSI6Imh0dHBzOi8vc2hpZnRtYXRlMy0wLm9ucmVuZGVyLmNvbSIsInNlc3Npb25JbmRleCI6N30seyJrZXkiOiJzY2hlZHVsZV9pZCIsInZhbHVlIjoiMSIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoiMSIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiMSIsInNlc3Npb25JbmRleCI6OH1d)

## 🖥️ CLI Reference
ShiftMate exposes a series of CLI tools through wsgi.py.
Run them using:
```bash
flask <group> <command>
```
### 🔐 Authentication
- `flask auth login <username> <password>` — login and save a JWT token for CLI use
- `flask auth logout <username>` — logout (removes saved token file)

### 👥 User Management
- `flask user create <username> <password> <role>` — create a user (role: `admin` or `staff`)
- `flask user list [string|json]` — list users in text or JSON format

### 🕒 Shift Management
- `flask shift schedule <staff_id> <schedule_id> <start_iso> <end_iso>` - Schedule a shift (admin only)

```bash
Example:
flask shift schedule 2 1 2025-10-01T09:00:00 2025-10-01T17:00:00
````

- `flask shift roster` - View Roster (staff only)

- `flask shift clockin <shift_id>
flask shift clockout <shift_id>` - Clock in / out (staff only)

- `flask shift report` - View Shift Report (admin)

### 📅 Schedule Management
- `flask schedule create <name>` — create a schedule (admin)

- `flask schedule list` — list schedules (admin)

- `flask schedule view <schedule_id>` — view a schedule and its shifts (admin)

- `flask schedule auto <schedule_id> <strategy> [--days N] [--shifts-per-day N] [--shift-type <type>]` — auto-generate shifts into an existing schedule (admin)
    - Example strategies: `even-distribute`, `minimize-days`, `preference-based`, `day-night-distribute`
    - Example: `flask schedule auto 1 even-distribute --days 14 --shifts-per-day 2 --shift-type mixed`

### 🎛️ Preferences (Staff Configuration)
_Each staff member may define:_

| Field                   | Description                  |
| ----------------------- | ---------------------------- |
| `preferred_shift_types` | e.g. `['morning','evening']` |
| `skills`                | list of strings              |
| `unavailable_days`      | integers `0–6` (Sunday=0)    |
| `max_hours_per_week`    | integer hours limit          |

The `prefs` CLI uses flags for each preference field. Examples:
```bash
# set preferences using CLI flags
flask prefs set <staff_id> --preferred "morning,evening" --skills "cashier" --unavailable "0,6" --max_hours 40

# get preferences
flask prefs get <staff_id>

# list all preferences
flask prefs list
```

Note: the `--preferred`, `--skills`, and `--unavailable` flags accept comma-separated values when using the CLI; the controllers accept Python lists when called from code.


# 🔄 Complete CLI Workflow (Recommended)
This section provides a full example run of the system from DB initialization → scheduling → staff usage → reporting, application using the CLI. You can run the commands with `flask` or `python -m flask` from the project root.

1) Initialize Database

```bash
flask init
```

2) Create admin & staff users

```bash
flask user create admin adminpass admin
flask user create jane janepass staff
flask user create bobstaff bobpass staff
flask user create alice alicepass staff
```

3) Verify users

```bash
flask user list
```

4) Login as Admin

```bash
flask auth login admin adminpass
flask auth whoami
```

5) Create schedules

```bash
flask schedule create "December Schedule"
flask schedule create "January Schedule"
```

6) Auto-generate shifts into schedule (example)

```bash
flask schedule auto 1 even-distribute --days 3 --shifts-per-day 2
flask schedule auto 2 preference-based --days 2 --shifts-per-day 3
```

7) View schedules

```bash
flask schedule list
flask schedule view 1
flask schedule view 2
```

8) Set preferences for staff

```bash
flask prefs set 2 --preferred "morning,day" --skills "cashier" --max_hours 40 --unavailable "1,3"
flask prefs set 3 --preferred "evening" --skills "stocking" --max_hours 35 --unavailable "0,6"
```

9) Verify preferences

```bash
flask prefs get 2
flask prefs get 3
flask prefs list
```

10) Manual shift scheduling (admin)

```bash
flask shift schedule 2 1 "2024-12-25T09:00:00" "2024-12-25T17:00:00"
flask shift schedule 3 1 "2024-12-26T14:00:00" "2024-12-26T22:00:00"
```

11) View updated schedule

```bash
flask schedule view 1
```

12) Admin report

```bash
flask shift report
```

13) Logout admin

```bash
flask auth logout
```

14) Staff flows (login, roster, clock in/out, logout)

```bash
# Jane
flask auth login jane janepass
flask auth whoami
flask shift roster
flask shift clockin 1
flask shift clockout 1
flask shift roster
flask auth logout

# Bobstaff
flask auth login bobstaff bobpass
flask auth whoami
flask shift roster
flask shift clockin 3
flask shift clockout 3
flask shift roster
flask auth logout

# Alice
flask auth login alice alicepass
flask auth whoami
flask shift roster
flask shift clockin 2
flask shift clockout 2
flask shift roster
flask auth logout
```

15) Final admin checks

```bash
flask auth login admin adminpass
flask shift report
flask schedule view 1
flask schedule view 2
flask user list
flask prefs get 2
flask prefs get 3
flask prefs list
```

16) Final logout

```bash
flask auth logout
```
# User Management

Create Users

After flask type user create then add the username, the password and the role of the user (either admin, staff or user)

```bash
flask user create admin1 adminpass admin
```
List users
```bash
flask user list string
flask user list json
```
# Managing shifts

To Schedule shifts (Admin only)

After flask type shift  schedule the staff id, the schedule idand the start and end of the shift in the ISO 8601 DateTime with time format( can copy the formant below and edit it)

```bash
flask shift schedule 2 1 2025-10-01T09:00:00 2025-10-01T17:00:00
```
View Roster (Staff only)

After flask type shift roster to for the logged in staff

```bash
flask shift roster 
```
Clockin and Clockout(Staff only)

After flask type shift clockin or clockoutand the shift id

```bash
flask shift clockin 1
flask shift clockout 1
```

Shift Report (Admin only)

After flask  type shift report 

```bash
flask shift report 
```

# Managing schedule

Create Schedule(Admin only)

After flask type schedule, create and the title 

```bash
flask schedule create "April Week 2" 
```

List All Schedules(Admin only)

After flask  type schedule  list 

```bash
flask schedule list 
```
View a Schedule (Admin only)

After flask type schedule view and the schedule id 

```bash
flask schedule view 1 
```

# Preferences
Per-staff preferences influence scheduling decisions. Stored fields:
- `preferred_shift_types` — list of strings (e.g. `['morning','evening']`)
- `skills` — list of strings
- `unavailable_days` — list of weekday integers `0..6` (Sunday=0)
- `max_hours_per_week` — integer (0..168)

Use the controller helpers in `App/controllers/preferences.py`: `get_preferences(staff_id)` and `set_preferences(staff_id, ...)`.

CLI examples (use flags):
```bash
flask prefs set 5 --preferred "morning,evening" --skills "cashier" --unavailable "0,6" --max_hours 40
flask prefs get 5
```


# 🧪 Testing

The `wsgi.py` `test` group exposes a small helper for running the `User` test group:

```bash
# Run all user tests
flask test user

# Run all unit and integration tests
flask test-all

# Run only user unit tests
flask test user unit

# Run only user integration tests
flask test user int
```

For other groups (preferences, scheduling, etc.) use `pytest` directly and filter by test class name with `-k`.

```bash
# run all tests
pytest

# run only preference unit tests (from `App/tests/test_app.py`)
pytest -k PreferencesUnitTests

# run only preference integration tests
pytest -k PreferencesIntegrationTests
```



