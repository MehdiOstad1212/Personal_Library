def test_books_list_response_401(anon_client):
    response = anon_client.get("/api/v1/books")
    assert response.status_code == 401

def test_books_list_response_200(auth_client):
    response = auth_client.get("/api/v1/books")
    assert response.status_code == 200
    assert len(response.json())> 0

def test_tasks_detail_response_200 (auth_client, random_book):
    book_obj = random_book
    response = auth_client.get(f"/api/v1/books/{book_obj.author}")
    assert response.status_code == 200

def test_tasks_detail_response_404 (auth_client):
    response = auth_client.get("/api/v1/books/'mona'")
    assert response.status_code == 404