from config import API_URL, DATA_FEEDS_DIR, SQUAD_FEEDS_DIR, OTHER_TOURNAMENT_DIR
from utils import fetch_data,save_json

def collect_data():
    # Data collection from API
    data = fetch_data(API_URL)

    # Save data in separate directories
    save_json(data, f"{DATA_FEEDS_DIR}/data.json")
    save_json(data["squad"], f"{SQUAD_FEEDS_DIR}/squad.json")
    save_json(data["other"], f"{OTHER_TOURNAMENT_DIR}/other.json")

    print("Data collection completed successfully!")
