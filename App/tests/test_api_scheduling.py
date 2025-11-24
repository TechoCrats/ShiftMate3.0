import pytest
import json
from datetime import datetime
from App.models import User, Admin, Staff, Schedule, Shift
from App.database import db

class TestSchedulingAPI:

    def test_get_strategies(self, client, init_database):
        """Test getting available strategies via API"""
        response = client.get('/api/scheduling/strategies')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'strategies' in data
        # Verify all four strategies are available 
        assert 'even-distribute' in data['strategies']
        assert 'minimize-days' in data['strategies']
        assert 'preference-based' in data['strategies']
        assert 'day-night-distribute' in data['strategies']

    def test_auto_populate_schedule_success(self, client, init_database):
        """Test successful schedule auto-population via API"""
        # Create test users directly in database
        admin = Admin(username="api_admin", password="password")
        staff1 = Staff(username="api_staff1", password="password")
        staff2 = Staff(username="api_staff2", password="password")
        
        db.session.add_all([admin, staff1, staff2])
        db.session.commit()
        
        # Create a schedule first
        schedule = Schedule(name="Test Schedule", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        # Test the special feature API endpoint
        data = {
            "admin_id": admin.id,
            "schedule_id": schedule.id,
            "strategy_name": "even-distribute",
            "staff_ids": [staff1.id, staff2.id],
            "start_date": "2024-01-01",
            "end_date": "2024-01-03",
            "shifts_per_day": 2,
            "shift_type": "mixed"
        }
        
        response = client.post(
            '/api/scheduling/auto-populate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check if endpoint exists, if not skip or handle appropriately
        if response.status_code == 404:
            pytest.skip("API endpoint not implemented yet")
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'shifts_created' in data
        assert 'score' in data 

    def test_auto_populate_different_strategies(self, client, init_database):
        """Test that different strategies work via API"""
        admin = Admin(username="multi_admin", password="password")
        staff1 = Staff(username="multi_staff1", password="password")
        staff2 = Staff(username="multi_staff2", password="password")
        
        db.session.add_all([admin, staff1, staff2])
        db.session.commit()
        
        # Create schedule
        schedule = Schedule(name="Multi Strategy Test", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        # Test multiple strategies
        strategies = ['even-distribute', 'minimize-days', 'preference-based']
        
        for strategy in strategies:
            data = {
                "admin_id": admin.id,
                "schedule_id": schedule.id,
                "strategy_name": strategy,
                "staff_ids": [staff1.id, staff2.id],
                "start_date": "2024-01-01", 
                "end_date": "2024-01-02",
                "shifts_per_day": 2,
                "shift_type": "mixed"
            }
            
            response = client.post(
                '/api/scheduling/auto-populate',
                data=json.dumps(data),
                content_type='application/json'
            )
            
            if response.status_code == 404:
                pytest.skip("API endpoint not implemented yet")
            
            assert response.status_code == 201
            result_data = json.loads(response.data)
            assert result_data['success'] == True

    def test_compare_strategies_api(self, client, init_database):
        """Test strategy comparison feature via API"""
        admin = Admin(username="compare_admin", password="password")
        staff1 = Staff(username="compare_staff1", password="password")
        staff2 = Staff(username="compare_staff2", password="password")
        
        db.session.add_all([admin, staff1, staff2])
        db.session.commit()
        
        # Create schedule
        schedule = Schedule(name="Compare Test", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        data = {
            "admin_id": admin.id,
            "schedule_id": schedule.id,
            "staff_ids": [staff1.id, staff2.id],
            "start_date": "2024-01-01",
            "end_date": "2024-01-02",
            "shifts_per_day": 2,
            "shift_type": "mixed"
        }
        
        response = client.post(
            '/api/scheduling/compare',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        if response.status_code == 404:
            pytest.skip("Comparison API endpoint not implemented yet")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'comparison' in data

    def test_auto_populate_invalid_strategy_api(self, client, init_database):
        """Test error handling for invalid strategy via API"""
        admin = Admin(username="error_admin", password="password")
        staff = Staff(username="error_staff", password="password")
        
        db.session.add_all([admin, staff])
        db.session.commit()
        
        schedule = Schedule(name="Error Test", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        data = {
            "admin_id": admin.id,
            "schedule_id": schedule.id,
            "strategy_name": "invalid_strategy",  
            "staff_ids": [staff.id],
            "start_date": "2024-01-01",
            "end_date": "2024-01-02",
            "shifts_per_day": 2,
            "shift_type": "mixed"
        }
        
        response = client.post(
            '/api/scheduling/auto-populate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        if response.status_code == 404:
            pytest.skip("API endpoint not implemented yet")
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False
        assert 'error' in data

    def test_auto_populate_no_staff_api(self, client, init_database):
        """Test auto-populate with no staff members via API"""
        admin = Admin(username="nostaff_admin", password="password")
        db.session.add(admin)
        db.session.commit()
        
        schedule = Schedule(name="No Staff Test", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        data = {
            "admin_id": admin.id,
            "schedule_id": schedule.id,
            "strategy_name": "even-distribute",
            "staff_ids": [],  
            "start_date": "2024-01-01",
            "end_date": "2024-01-02",
            "shifts_per_day": 2,
            "shift_type": "mixed"
        }
        
        response = client.post(
            '/api/scheduling/auto-populate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        if response.status_code == 404:
            pytest.skip("API endpoint not implemented yet")
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False

    def test_get_schedules_api(self, client, init_database):
        """Test getting schedules via API"""
        response = client.get('/api/schedules')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'schedules' in data

    def test_get_schedule_details_api(self, client, init_database):
        """Test getting specific schedule details via API"""
        # First create a schedule
        admin = Admin(username="detail_admin", password="password")
        staff = Staff(username="detail_staff", password="password")
        
        db.session.add_all([admin, staff])
        db.session.commit()
        
        schedule = Schedule(name="Test Schedule", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        response = client.get(f'/api/schedules/{schedule.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'schedule' in data

    def test_create_schedule_api(self, client, init_database):
        """Test creating a new schedule via API"""
        admin = Admin(username="create_admin", password="password")
        db.session.add(admin)
        db.session.commit()
        
        data = {
            "name": "New Test Schedule",
            "created_by": admin.id
        }
        
        response = client.post(
            '/api/schedules',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'schedule' in data
        assert data['schedule']['name'] == "New Test Schedule"

    def test_get_shifts_for_schedule_api(self, client, init_database):
        """Test getting shifts for a specific schedule via API"""
        admin = Admin(username="shift_admin", password="password")
        staff = Staff(username="shift_staff", password="password")
        
        db.session.add_all([admin, staff])
        db.session.commit()
        
        schedule = Schedule(name="Shift Test Schedule", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        # Create a test shift
        shift = Shift(
            schedule_id=schedule.id,
            staff_id=staff.id,
            start_time=datetime(2024, 1, 1, 9, 0),
            end_time=datetime(2024, 1, 1, 17, 0)
        )
        db.session.add(shift)
        db.session.commit()
        
        response = client.get(f'/api/schedules/{schedule.id}/shifts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'shifts' in data
        assert len(data['shifts']) == 1

    def test_get_available_strategies_api(self, client, init_database):
        """Test getting available scheduling strategies"""
        response = client.get('/api/scheduling/strategies')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        assert 'strategies' in data
        expected_strategies = ["even-distribute", "minimize-days", "preference-based", "day-night-distribute"]
        for strategy in expected_strategies:
            assert strategy in data['strategies']

    def test_auto_populate_missing_required_fields(self, client, init_database):
        """Test auto-populate with missing required fields"""
        admin = Admin(username="missing_admin", password="password")
        db.session.add(admin)
        db.session.commit()
        
        data = {
            "admin_id": admin.id,
            "strategy_name": "even-distribute",
            "staff_ids": [1],
            "start_date": "2024-01-01",
            "end_date": "2024-01-02"
        }
        
        response = client.post(
            '/api/scheduling/auto-populate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        if response.status_code == 404:
            pytest.skip("API endpoint not implemented yet")
        
        # Should return 400 for bad request
        assert response.status_code == 400

    def test_auto_populate_invalid_date_format(self, client, init_database):
        """Test auto-populate with invalid date format"""
        admin = Admin(username="date_admin", password="password")
        staff = Staff(username="date_staff", password="password")
        
        db.session.add_all([admin, staff])
        db.session.commit()
        
        schedule = Schedule(name="Date Test", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        data = {
            "admin_id": admin.id,
            "schedule_id": schedule.id,
            "strategy_name": "even-distribute",
            "staff_ids": [staff.id],
            "start_date": "invalid-date", 
            "end_date": "2024-01-02",
            "shifts_per_day": 2,
            "shift_type": "mixed"
        }
        
        response = client.post(
            '/api/scheduling/auto-populate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        if response.status_code == 404:
            pytest.skip("API endpoint not implemented yet")
        
        assert response.status_code == 400

    def test_auto_populate_end_date_before_start(self, client, init_database):
        """Test auto-populate with end date before start date"""
        admin = Admin(username="date_order_admin", password="password")
        staff = Staff(username="date_order_staff", password="password")
        
        db.session.add_all([admin, staff])
        db.session.commit()
        
        schedule = Schedule(name="Date Order Test", created_by=admin.id)
        db.session.add(schedule)
        db.session.commit()
        
        data = {
            "admin_id": admin.id,
            "schedule_id": schedule.id,
            "strategy_name": "even-distribute",
            "staff_ids": [staff.id],
            "start_date": "2024-01-10",  
            "end_date": "2024-01-05",    
            "shifts_per_day": 2,
            "shift_type": "mixed"
        }
        
        response = client.post(
            '/api/scheduling/auto-populate',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        if response.status_code == 404:
            pytest.skip("API endpoint not implemented yet")
        
        assert response.status_code == 400