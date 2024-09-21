from model.object import BaseObject


def test_id_increment():
    data = {
        'name': 'something1',
    }

    s1 = BaseObject(**data)

    assert s1.id == 'BaseObject_1'

    data = {
        'name': 'something2',
    }

    s2 = BaseObject(**data)
    assert s2.id == 'BaseObject_2'
