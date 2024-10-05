import pytest

from dnd_engine.model import event as ev


@pytest.fixture
def deque():
    return ev.create_deque()


def test_publish_to_deque(deque):
    assert len(deque) == 0
    ev.publish_to_deque(source="test source", msg="test message", dq=deque)
    assert len(deque) == 1


def test_exec_on_deque(deque):
    ev.publish_to_deque(source="test source", msg="test message", dq=deque)

    def msg_len(e):
        return len(e.msg)

    r = ev.exec_on_deque(msg_len, dq=deque)
    assert r == [12]


def test_get_deque(deque):
    ev.publish_to_deque(source="test source", msg="test message", dq=deque)
    r = ev.get_deque(dq=deque)
    assert r == ["test source: test message"]
