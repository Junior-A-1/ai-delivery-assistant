from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Body
# from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import re
# import requests

orders= {}
app = FastAPI()
# client = OpenAI(api_key= "YOUR-KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/") 
def home():
    return {"message" : "Server is running!"}

class DriverStatus(BaseModel):
    order_id : str
    status: str
    lat: float
    lng: float

@app.post("/update-driver-status")
def update_status(data: DriverStatus):
    orders[data.order_id] = {
        "status": data.status,
        "lat": data.lat,
        "lng": data.lng
    }
    return{
        "message":"Status stored automatically"
    }
@app.get("/get-order/{order_id}")
def get_order(order_id:str):
    return orders.get(order_id, {"error":"Orders not found"})



@app.post("/ask-ai")
def ask_ai(order_id:str = Body(...) , question: str = Body(...)):
    order = orders.get(order_id)
    if not order:
        return {"error":" Order is not found"}
    status = order["status"]
    question = question.lower()
    lat = order['lat']
    lng = order['lng']
    time_match = re.search(r'\d+', status)

    if time_match:
        extracted_time = time_match.group()
        eta = f"{extracted_time} minutes"
    else:
    # Case 1: Waiting at restaurant
        if "waiting" in status.lower() or "restaurant" in status.lower():
            eta = "10-15minutes "

    # Case 2: On the way
        elif "on the way" in status.lower():
            eta = "5-10 minutes"

    # Case 3: Delivered
        elif "delivered" in status.lower():
            eta = "0 minutes"
        else:
            eta = "unknown"

    


# == OPTION 1: Google Maps API (COMMENTED - FOR FUTURE USE) =====

# url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key=YOUR_API_KEY"
# response = requests.get(url)
# data = response.json()
#
# if data["results"]:
#     location_name = data["results"][0]["formatted_address"]
# else:
#     location_name = "unknown location"


# = OPTION 2: Manual Mapping (CURRENTLY ACTIVE -> FREE)
    # Location message
    if lat == -33.8688:
        location_message = "Driver is near Sydney CBD"
    else:
        location_message = f"Driver is near ({lat}, {lng})"

#AI PROMPT (FUTURE USE)
    prompt = f"""
    Driver status: {order['status']}
    Customer question: {question}

    Give a helpful response.
    """

#OPENAI 
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "user", "content": prompt}
    #     ]
    # )

    # return {
    #     "ai_response": response.choices[0].message.content
    # }


#RESPONSE (NO BILLING)
    return {
        "source": "rule-based + extracted",
        "ai_response": f"{location_message}. Your rider is currently at the restaurant waiting for your order. Estimated delivery time is {eta}."
    }




    


