from fastapi import FastAPI, HTTPException, status, Body
from schemas import Ship, Response, ShipmentStatus, UpdateShipment

app = FastAPI(title="FastAPI Fundamentals - In-Memory CRUD")

shipments = {
    1270: {"weight": 12.5, "content": "wooden table", "status": "delivered"},
    1271: {"weight": 13.5, "content": "toys", "status": "pending"},
    1272: {"weight": 10.2, "content": "chair", "status": "shipped"},
    1273: {"weight": 5.1, "content": "books", "status": "pending"},
    1274: {"weight": 22.0, "content": "refrigerator", "status": "delivered"},
    1275: {"weight": 3.7, "content": "clothes", "status": "shipped"},
    1276: {"weight": 8.9, "content": "shoes", "status": "pending"},
    1277: {"weight": 15.0, "content": "monitor", "status": "delivered"},
    1278: {"weight": 6.3, "content": "keyboard", "status": "shipped"},
    1279: {"weight": 1.1, "content": "mouse", "status": "pending"},
}


@app.get("/shipments")
def get_all_shipments():
    return shipments


# find latest shipment by highest id
@app.get("/shipments/latest")
def get_latest_shipment():
    if not shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No shipments available",
        )
    latest_id = max(shipments.keys())
    return {"id": latest_id, **shipments[latest_id]}


@app.get("/shipments/{shipment_id}")
def get_shipment_by_id(shipment_id: int):
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment with that id not found",
        )
    return shipments[shipment_id]


# filter and verify matching record
@app.get("/shipments/verify/{shipment_id}")
def get_by_id_weight(shipment_id: int, weight: float):
    if weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight should be greater than 0",
        )
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment with that id not found",
        )
    shipment = shipments[shipment_id]
    if shipment["weight"] != weight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weight does not match records",
        )
    return shipment


# creating a record with raw fastapi Body parameters
@app.post("/shipments/raw")
def create_shipment_raw(weight: float = Body(...), content: str = Body(...)):
    if weight <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weight must be greater than zero",
        )
    new_id = max(shipments.keys(), default=1000) + 1
    new_item = {"weight": weight, "content": content, "status": "placed"}
    shipments[new_id] = new_item
    return {"id": new_id, **shipments[new_id]}


# creating a record using pydantic schema validation
@app.post("/new-ship", response_model=Response)
def create_shipment_schema(data: Ship):
    new_id = max(shipments.keys(), default=1000) + 1
    new_content = {
        "id": new_id,
        "weight": data.weight,
        "content": data.content,
        "status": data.status.value if hasattr(data.status, "value") else str(data.status),
    }
    shipments[new_id] = new_content
    return shipments[new_id]


@app.put("/shipments/{shipment_id}")
def update_shipment(shipment_id: int, weight: float, content: str):
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    shipments[shipment_id].update({"weight": weight, "content": content})
    return {"message": f"Shipment #{shipment_id} updated successfully", "shipment": shipments[shipment_id]}


# updating record using pydantic schema
@app.put("/update-shipment/{shipment_id}")
def update_shipment_with_schema(shipment_id: int, data: UpdateShipment):
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    shipments[shipment_id] = {
        "id": shipment_id,
        "weight": data.weight,
        "content": data.content,
        "status": ShipmentStatus.shipped.value,
    }
    return shipments[shipment_id]


@app.delete("/shipments/{shipment_id}")
def delete_shipment(shipment_id: int):
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found",
        )
    shipments.pop(shipment_id)
    return {"message": f"Shipment #{shipment_id} deleted successfully"}
