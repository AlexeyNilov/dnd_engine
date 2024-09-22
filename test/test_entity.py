from model.entity import Entity


def test_id_increment():
    data = {
        'name': 'something1',
    }

    s1 = Entity(**data)

    assert s1.id == 'Entity_1'

    data = {
        'name': 'something2',
    }

    s2 = Entity(**data)
    assert s2.id == 'Entity_2'
