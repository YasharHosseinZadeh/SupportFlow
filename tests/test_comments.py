
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Post
def test_create_comment(test_ticket,test_user):
    response = client.post(
        f"/tickets/{test_ticket.id}/comments",
        json={
            "content": "test comment",
            "author_id": test_user.id,
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["id"], int)
    assert data["content"] == "test comment"
    assert data["ticket_id"] == test_ticket.id
    assert data["author_id"] == test_user.id

def test_create_comment_wrong_ticket_id(test_user):
    response = client.post(
        "/tickets/999/comments",
        json={
            "content" : "test comment",
            "author_id" : test_user.id
        }

    )
    assert response.status_code == 404
    assert response.json() == {"detail" : "User or Ticket not found"}


def test_create_comment_wrong_author_id(test_ticket):
    response = client.post(
            f"/tickets/{test_ticket.id}/comments",
            json={
                "content" : "test comment",
                "author_id" : 999
            }

        )
    assert response.status_code == 404
    assert response.json() == {"detail" : "User or Ticket not found"}



# Get
def test_get_comments_by_ticket_id(test_ticket,test_user):
    response = client.post(
        f"/tickets/{test_ticket.id}/comments",
        json = {
            "content": "test comment",
            "author_id": test_user.id
        }
    )
    response = client.post(
        f"/tickets/{test_ticket.id}/comments",
        json = {
            "content": "test comment2",
            "author_id": test_user.id
        }
    )
    response = client.get(
        f"/tickets/{test_ticket.id}/comments"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert isinstance(data, list)
    assert data[0]["content"] == "test comment"
    assert data[0]["ticket_id"] == test_ticket.id
    assert data[0]["author_id"] == test_user.id
    assert data[1]["content"] == "test comment2"
    assert data[1]["ticket_id"] == test_ticket.id
    assert data[1]["author_id"] == test_user.id


def test_get_comments_wrong_ticket_id(test_user):
    response = client.get(
        "/tickets/999/comments"
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User or Ticket not found"}


def test_get_comment_by_comment_id(test_ticket , test_user):
    response = client.post(
        f"/tickets/{test_ticket.id}/comments",
        json = {
            "content": "test comment",
            "author_id": test_user.id
        }
    )

    comment_id = response.json()["id"]

    response = client.get(
        f"/comments/{comment_id}"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == comment_id
    assert data["content"] == "test comment"
    assert data["ticket_id"] == test_ticket.id
    assert data["author_id"] == test_user.id


def test_get_comment_by_not_found():
    response = client.get("/comments/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}

# Patch
def test_update_comment(test_ticket,test_user):
    response = client.post(
        f"/tickets/{test_ticket.id}/comments",
        json={
            "content": "This is a test comment",
            "author_id": test_user.id
        }
    )
    comment_id = response.json()["id"]

    response = client.patch(
        f"/comments/{comment_id}",
        json={
            "content": "This is a new test comment",
        }
    )
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == comment_id
    assert data["content"] == "This is a new test comment"
    assert data["ticket_id"] == test_ticket.id
    assert data["author_id"] == test_user.id


def test_update_comment_not_found():
    response = client.patch(
        "/comments/999",
        json = {"content": "This is a new test comment"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}


# Delete
def test_delete_comment(test_ticket,test_user):
    response = client.post(
        f"/tickets/{test_ticket.id}/comments",
        json={
            "content": "This is a test comment",
            "author_id": test_user.id
        }
    )
    comment_id = response.json()["id"]

    response = client.delete(
        f"/comments/{comment_id}")
    assert response.status_code == 204
    response = client.get(
        f"/comments/{comment_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}


def test_delete_comment_not_found():
    response = client.delete("/comments/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Comment not found"}
