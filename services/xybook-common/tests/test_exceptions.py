from fastapi import HTTPException

from xybook_common.exceptions import ConflictError, NotFoundError, ServiceError


def test_service_error():
    e = ServiceError("test")
    assert e.detail == "test"
    assert e.status_code == 500
    assert isinstance(e, HTTPException)


def test_not_found_error():
    e = NotFoundError("item not found")
    assert e.detail == "item not found"
    assert e.status_code == 404
    assert isinstance(e, HTTPException)


def test_conflict_error():
    e = ConflictError("duplicate item")
    assert e.detail == "duplicate item"
    assert e.status_code == 409
    assert isinstance(e, HTTPException)
