"""Tests for the Patient model."""


def test_create_person():
    from inflammation.models import Person

    name = 'Alice'
    p = Person(name=name)

    assert p.name == name


def test_create_patient():
    from inflammation.models import Patient

    name = 'Alice'
    p = Patient(name=name)

    assert p.name == name


def test_create_doctor():
    from inflammation.models import Doctor

    name = 'Alice'
    d = Doctor(name=name)

    assert d.name == name
    assert d.patients == []


def test_add_patient():
    from inflammation.models import Doctor, Patient

    name = 'Alice'
    d = Doctor(name=name)

    p1 = Patient(name="Bob")

    assert len(d.patients) == 0

    d.add_patient(p1)

    assert len(d.patients) == 1
    assert d.patients[0] == p1

    p2 = Patient(name="Charlie")

    d.add_patient(p2)

    assert len(d.patients) == 2
    assert d.patients == [p1, p2]
