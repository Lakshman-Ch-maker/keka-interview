import logging
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ------- Logger -------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("app")

# --------------Models -------
class TicketIn(BaseModel):
    vehicle_number: str = Field(min_length = 1)
    vehicle_type : str = Field(min_length = 1)
class Slot(BaseModel):
    vehicle_type: str
    vehicle_number : str
    slot_number : int

# ----- Storage --------
parking_lot = {str : {}}

# -------------Service (business rules)  ----------

def confirm_parking(req: TicketIn):
    if req.vehicle_type.lower() != "car" or req.vehicle_type != "bike":
        raise ValueError("vehicle type should be a \'car\' or \'bike\' .")
    if req.slots[req.vehicle_type.lower()] <= 0:
        raise ValueError("free slots are not available")
    vid = str(uuid.uuid4())
    parking_lot[req.vehicle_type.lower()].append(vid)
    log.info("vehicle id=%s booked a slot", vid)
    return {"ticketid" : vid, "slot" : , "vehicle_type" : req.vehicle_type.lower(), "status": "PARKED"}


# -------  HTTP Layer ---------
app = FastAPI()

@app.post("/entry", status_code = 201)
def create_entry(req: TicketIn):
    try:
        return confirm_parking(req)
    except ValueError as e:
        log.warning("Bad Request: %s", e)
        raise HTTPException(status_code=409, detail=str(e))

@app.post("/exit/{ticket_id, minutes_parked}")
def leave_parking(ticket_id: str):
    if ticket_id not in parking_lot:
        raise HTTPException(status_code = 404, detail="Vehicle not found")
    return 
        