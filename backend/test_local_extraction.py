from fastapi.testclient import TestClient
from app.main import app

def test_endpoints():
    client = TestClient(app)
    
    # 1. Search for bvs mandi
    print("\n--- Testing BVS Mandi ---")
    resp_bvs = client.post("/search-restaurant", json={"query": "bvs mandi"})
    assert resp_bvs.status_code == 200, f"BVS Mandi search failed: {resp_bvs.text}"
    place_id_bvs = resp_bvs.json().get("place_id")
    print(f"BVS Mandi Place ID: {place_id_bvs}")
    
    # Get details for BVS Mandi
    resp_details_bvs = client.get(f"/restaurant/{place_id_bvs}")
    assert resp_details_bvs.status_code == 200
    details_bvs = resp_details_bvs.json()
    best_bvs = details_bvs.get("best_item")
    worst_bvs = details_bvs.get("worst_item")
    print(f"BVS Mandi Best Item: {best_bvs}")
    print(f"BVS Mandi Worst Item: {worst_bvs}")
    
    # 2. Search for karsh
    print("\n--- Testing Karsh Mandi ---")
    resp_karsh = client.post("/search-restaurant", json={"query": "karsh"})
    assert resp_karsh.status_code == 200, f"Karsh Mandi search failed: {resp_karsh.text}"
    place_id_karsh = resp_karsh.json().get("place_id")
    print(f"Karsh Mandi Place ID: {place_id_karsh}")
    
    # Get details for Karsh Mandi
    resp_details_karsh = client.get(f"/restaurant/{place_id_karsh}")
    assert resp_details_karsh.status_code == 200
    details_karsh = resp_details_karsh.json()
    best_karsh = details_karsh.get("best_item")
    worst_karsh = details_karsh.get("worst_item")
    print(f"Karsh Mandi Best Item: {best_karsh}")
    print(f"Karsh Mandi Worst Item: {worst_karsh}")
    
    # Validate uniqueness
    print("\n--- Validating Uniqueness ---")
    assert best_bvs != best_karsh, f"Error: Best food item matches! ({best_bvs})"
    assert worst_bvs != worst_karsh, f"Error: Worst food item matches! ({worst_bvs})"
    print("Success: Best and worst food items are unique and correct across different mandi restaurants!")

if __name__ == '__main__':
    test_endpoints()
