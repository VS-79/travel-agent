import time
import httpx
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.vector_store import vector_store

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TravelAgentBot/1.0; +http://localhost; educational-project)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}

CITY_PAGES = {
    "Tokyo": ["Tokyo", "Shinjuku", "Asakusa", "Shibuya"],
    "Paris": ["Paris", "Montmartre", "Louvre_Museum", "Eiffel_Tower"],
    "Singapore": ["Singapore", "Marina_Bay_Sands", "Sentosa", "Chinatown,_Singapore"],
    "London": ["London", "Tower_of_London", "Covent_Garden", "British_Museum"],
    "Bangkok": ["Bangkok", "Wat_Phra_Kaew", "Chatuchak_Weekend_Market", "Khao_San_Road"],
}

def fetch_page(page_title: str, city: str) -> dict:
    try:
        time.sleep(2)
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "titles": page_title.replace("_", " "),
            "prop": "extracts",
            "explaintext": True,
            "exsectionformat": "plain",
            "format": "json",
            "redirects": 1,
            "exlimit": 1,
        }
        response = httpx.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=20,
            follow_redirects=True
        )

        print(f"DEBUG: HTTP {response.status_code} for {page_title}")

        if response.status_code == 200:
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id != "-1":
                    extract = page_data.get("extract", "")
                    if extract and len(extract) > 100:
                        print(f"DEBUG: Got {len(extract)} chars for {page_title}")
                        return {
                            "text": extract[:5000],
                            "source": f"https://en.wikipedia.org/wiki/{page_title}",
                            "city": city,
                            "topic": page_title.replace("_", " ")
                        }
            print(f"DEBUG: No content found for {page_title}")
            return None
        else:
            print(f"DEBUG: Failed with status {response.status_code}")
            return None

    except Exception as e:
        print(f"DEBUG: Error for {page_title}: {e}")
        return None

def chunk_documents(documents: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["text"])
        for split in splits:
            chunks.append({
                "text": split,
                "source": doc["source"],
                "city": doc["city"],
                "topic": doc["topic"]
            })
    print(f"DEBUG: Created {len(chunks)} chunks from {len(documents)} documents")
    return chunks

def fetch_city_content(city: str) -> list:
    documents = []
    for title in CITY_PAGES.get(city, [city]):
        doc = fetch_page(title, city)
        if doc:
            documents.append(doc)
    return documents

def build_index(cities: list = None):
    cities = cities or list(CITY_PAGES.keys())
    all_chunks = []
    for city in cities:
        print(f"\nDEBUG: Processing city - {city}")
        documents = fetch_city_content(city)
        chunks = chunk_documents(documents)
        all_chunks.extend(chunks)
        print(f"DEBUG: {city} complete - {len(chunks)} chunks")
        time.sleep(3)

    if all_chunks:
        vector_store.add_documents(all_chunks)
        print(f"\nDEBUG: RAG index built with {len(all_chunks)} total chunks")
    else:
        print("DEBUG: No chunks to add — Wikipedia may be blocking your IP") 