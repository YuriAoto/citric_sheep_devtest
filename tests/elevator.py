import elevator_model


def test_create():
    elevator = elevator_model.Elevator(None)
    assert elevator.vacant
    assert not elevator.floor

def test_operate():
    elevator = elevator_model.Elevator(None)
    elevator._goto(4)
    assert elevator.floor == 4
