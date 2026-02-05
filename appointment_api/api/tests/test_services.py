import pytest
from ..models.appointment import Appointment
from ..selectors.appointment_selector import AppointmentSelector

@pytest.mark.django_db
def test_conflict_detected(appointment, professional):
    conflict = AppointmentSelector.conflicts(
        Appointment.objects.filter(professional=professional),
        appointment_date=appointment.appointment_date
    )
    assert conflict is True
