"""Functional tests for customers"""
from hyperion.common import status


def test_create_new_customer(client, db_session):
    """Test should create a new customer"""
    # Arrange
    customer_data = {"name": "Customer 1", "isActive": True}

    # Act
    response = client.post("api/customers/", json=customer_data)
    response_data = response.get_json()

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response_data["name"] == customer_data["name"]


def test_get_list_customers_with_filters(client, db_session, make_customer_list):
    """Test should return list of customers"""
    # Arange
    customers = make_customer_list(10)

    # Act
    response = client.get("api/customers/?name=customer")
    response_data = response.get_json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data["items"]) == len(customers)


def test_get_customers_no_query_param_should_return_400(
    client, db_session, make_customer_list
):
    """Test should return customers"""
    # Arange
    customers = make_customer_list(10)

    # Act
    response = client.get("api/customers/")
    response_data = response.get_json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data["items"]) == len(customers)
