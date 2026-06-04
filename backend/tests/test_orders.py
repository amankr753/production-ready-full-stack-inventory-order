def test_order_deducts_stock_and_prevents_overselling(client, auth_headers):
    product = client.post(
        "/products",
        headers=auth_headers,
        json={
            "product_name": "Wireless Scanner",
            "sku_code": "SCAN-001",
            "description": "Handheld scanner",
            "category": "Hardware",
            "brand": "Acme",
            "purchase_price": 20,
            "selling_price": 45,
            "quantity_in_stock": 3,
            "reorder_level": 1,
            "product_image": None,
        },
    ).json()
    customer = client.post(
        "/customers",
        headers=auth_headers,
        json={"full_name": "Retail Buyer", "email": "buyer@example.com", "customer_type": "retail"},
    ).json()

    order = client.post(
        "/orders",
        headers=auth_headers,
        json={"customer_id": customer["id"], "items": [{"product_id": product["id"], "quantity": 2}], "tax_amount": 5, "discount": 0},
    )
    assert order.status_code == 201
    assert order.json()["total_amount"] == 95

    updated_product = client.get(f"/products/{product['id']}", headers=auth_headers)
    assert updated_product.json()["quantity_in_stock"] == 1

    oversell = client.post(
        "/orders",
        headers=auth_headers,
        json={"customer_id": customer["id"], "items": [{"product_id": product["id"], "quantity": 2}]},
    )
    assert oversell.status_code == 409
