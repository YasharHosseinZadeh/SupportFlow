from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Post
def test_create_ticket(test_user):
    response = client.post(
        "/tickets",
    json={
        "title": "Test Ticket",
        "description": "This is a test ticket",
        "customer_id": test_user.id
        }
    )
    data = response.json()
    assert response.status_code == 200

    assert data["title"] == "Test Ticket"
    assert data["description"] == "This is a test ticket"
    assert data["customer_id"] == test_user.id
    assert data["customer"] == {
        "id": test_user.id,
        "name": test_user.name,
        "email": test_user.email
    }
    assert isinstance(data["id"], int)


def test_create_ticket_wrong_customer():
    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "customer_id": 999
        }
    )

    assert response.status_code == 400
    assert response.json() == {"detail" : "Customer id is wrong"}



# Get
def test_get_tickets(test_user):
    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "customer_id": test_user.id
        }
    )
    response = client.get("/tickets")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert any(ticket["title"] == "Test Ticket" for ticket in data)
    assert len(data) == 1


def test_get_ticket_by_customer(test_user,test_user_2):
    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "customer_id": test_user.id
        }
    )
    response = client.post(
        "/tickets",
        json={
            "title": "test ticket",
            "description": "This is a test ticket",
            "customer_id": test_user_2.id
        }
    )

    response = client.get(
        "/tickets",
        params={
            "customer_id": test_user.id,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["customer_id"] == test_user.id
    assert data[0]["title"] == "Test Ticket"


def test_get_tickets_pagination(test_user):
    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket1",
            "description": "This is a test ticket1",
            "customer_id": test_user.id
        }
    )
    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket2",
            "description": "This is a test ticket2",
            "customer_id": test_user.id
        }
    )
    response = client.post(
        "/tickets",
        json={
            "title": "Test Ticket3",
            "description": "This is a test ticket3",
            "customer_id": test_user.id
        }
    )
    response = client.get(
        "/tickets",
        params={
            "page": 1,
            "limit": 2
        }
        )

    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

    response = client.get(
        "/tickets",
        params={
            "page": 2,
            "limit": 2
        }
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1


def test_get_ticket_by_id(test_user):
    response = client.post(
        "/tickets",
    json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "customer_id": test_user.id
        }
    )
    ticket_id = response.json()["id"]

    response = client.get(f"/tickets/{ticket_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == ticket_id
    assert data["title"] == "Test Ticket"
    assert data["description"] == "This is a test ticket"
    assert data["customer_id"] == test_user.id
    assert data["customer"] == {
        "id": test_user.id,
        "name": test_user.name,
        "email": test_user.email,
    }


def test_get_ticket_not_found():
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


# Patch
def test_update_ticket(test_user):
    response = client.post(
        "/tickets",
        json={
            "title" : "Old Title",
            "description" : "Old description",
            "customer_id" : test_user.id

        }
    )
    ticket_id = response.json()["id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={
            "title" : "New Title",
            "description" : "New description"
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == ticket_id
    assert data["title"] == "New Title"
    assert data["description"] == "New description"
    assert data["customer_id"] == test_user.id
    assert data["customer"] == {
        "id" : test_user.id,
        "name" : test_user.name,
        "email" : test_user.email,
    }


def test_update_ticket_not_found():
    response = client.patch(
        "/tickets/999",
        json={
            "title": "New Title",
            "description": "New description"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}


# Delete
def test_delete_ticket(test_user):
        response = client.post(
            "/tickets",
            json={
                "title" : "Old Title",
                "description" : "Old description",
                "customer_id" : test_user.id

            }
        )
        ticket_id = response.json()["id"]

        response = client.delete(f"/tickets/{ticket_id}")
        assert response.status_code == 204

        response = client.get(f"/tickets/{ticket_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "Ticket not found"}

def test_delete_ticket_not_found():
    response = client.delete("/tickets/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Ticket not found"}