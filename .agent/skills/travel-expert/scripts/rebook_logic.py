import json
import os
import time
import threading
import random
from amadeus import Client, ResponseError
from dotenv import load_dotenv

load_dotenv()

# High-Performance API Configuration
amadeus = Client(
    client_id=os.getenv('AMADEUS_API_KEY', 'YOUR_KEY_HERE'),
    client_secret=os.getenv('AMADEUS_API_SECRET', 'YOUR_SECRET_HERE')
)

results = {}

def fetch_flight_alternatives(pnr):
    """Parallel Thread 1: Amadeus Flight Search"""
    time.sleep(random.uniform(0.1, 0.4)) # Simulated latency
    results['flight'] = "FL-NEW-505"
    print("[REBOOKER] Parallel Task: Flight identified.")

def fetch_hotel_alternatives(location):
    """Parallel Thread 2: Amadeus Hotel Search"""
    time.sleep(random.uniform(0.1, 0.4)) # Simulated latency
    results['hotel'] = "Marriott Elite Suite"
    print("[REBOOKER] Parallel Task: Hotel secured.")

def perform_rebooking():
    """Atomic Turbo Rebooking Sequence"""
    try:
        if not os.path.exists('itinerary.json'):
            return
            
        with open('itinerary.json', 'r') as f:
            data = json.load(f)
            itinerary = data[0] if isinstance(data, list) else data
        
        if itinerary.get('status') == 'CANCELLED' or itinerary.get('status') == 'Confirmed':
            start_time = time.time()
            print(f"\n[URGENT] DISRUPTION RECOVERY ACTIVATED for PNR: {itinerary.get('pnr')}")
            
            # Simulated AI Intelligent Search Logic
            # We look for alternatives for the specific passenger
            p_name = itinerary.get('passenger_name', 'Alexander White')
            
            # Logic: If flight is the main transport, we might pivot to a High-Speed Train if available
            # or to a different Flight route.
            original_flight = itinerary.get('flight_no', '---')
            
            # Generate the "Alternative"
            if original_flight and original_flight != '---':
                new_flight = f"WT-ALT-{random.randint(100, 999)}"
                new_train = f"TRAIN-RECOV-{random.randint(10, 99)}"
                new_seat = f"{random.randint(1, 40)}{random.choice(['A','B','C','D'])}"
                new_status = "REBOOKED"
                new_gate = f"{random.choice(['A','B','C','D'])}{random.randint(1, 30)}"
            else:
                new_flight = f"WT-FIX-{random.randint(100, 999)}"
                new_train = "TRAIN-OFFLINE"
                new_seat = "7B"
                new_status = "REBOOKED"
                new_gate = "G9"

            # Finalize Update
            itinerary['status'] = new_status
            itinerary['flight_no'] = new_flight
            itinerary['train_no'] = new_train
            itinerary['seat'] = new_seat
            itinerary['gate'] = new_gate
            itinerary['boarding_time'] = "RETOUCHED"
            itinerary['recovery_time_ms'] = int((time.time() - start_time) * 1000)
            
            with open('itinerary.json', 'w') as f:
                json.dump([itinerary] if isinstance(data, list) else itinerary, f, indent=4)
            
            print(f"[REBOOKER] SUCCESS: Itinerary fixed in {itinerary['recovery_time_ms']}ms.")
            print(f"[FIXED]: Alternative Secured for {p_name}: {itinerary['flight_no']} / {itinerary['train_no']}")
            return True
            
    except Exception as e:
        print(f"[ERROR] Turbo Rebooking failed: {str(e)}")
        return False

if __name__ == "__main__":
    perform_rebooking()
