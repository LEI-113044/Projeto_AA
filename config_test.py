from dotenv import load_dotenv
import os
import requests
import random

# load .env
load_dotenv()

# ---------------------------------------------------------------------
# Check environment variables
# ---------------------------------------------------------------------
print("=" * 50)
print("Checking environment variables")
print("=" * 50)

required = [ 
    "TAVILY_API_KEY",
    "LANGSMITH_API_KEY",
    "LANGSMITH_ENDPOINT",
    "LANGSMITH_PROJECT",
    "OLLAMA_BASE_URL",
    "OLLAMA_API_KEY",
    "OLLAMA_MODEL"
]

ok = True
missing = []
for var in required:
    value = os.getenv(var)
    if not value:
        ok = False
        missing.append(var)
if not ok:
    print(f"X Missing environment variables: {missing}")
    exit()

print("OK - all environment variables loaded successfully.\n")


# ---------------------------------------------------------------------
# Tavily Test
# ---------------------------------------------------------------------
print("=" * 50)
print("Testing Tavily")
print("=" * 50)

try:
    from langchain_tavily import TavilySearch # type: ignore
    
    tavily = TavilySearch(max_results=2)
    results = tavily.invoke("What is LangChain?")
    
    print("OK - Tavily connected")

except Exception as e:
    print("X - Tavily failed")
    print(e)
    exit()

print()


# ---------------------------------------------------------------------
# Server Access Test
# ---------------------------------------------------------------------
print("=" * 50)
print("Testing the Access to the Server")
print("=" * 50)
base_url = os.environ["OLLAMA_BASE_URL"].rstrip("/")
api_key = os.environ["OLLAMA_API_KEY"]

try:
    response = requests.get(
    f"{base_url}/api/tags",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
        timeout=30,
    )

    response.raise_for_status()
    data = response.json()

    models = []
    for model in data.get("models", []):
        models.append(model["name"])
    if not models:
        raise RuntimeError("The server returned no models")
    print("OK - accessed the server")

except Exception as e:
    print("X - access to server failed: confirm that you are using either eduroam network or VPN access to it")
    exit()


print()

print("= " * 50)
print("Configuration Tests Successfully Completed")
print("= " * 50)



# ---------------------------------------------------------------------
# ELIZA
# ---------------------------------------------------------------------

# Source - https://stackoverflow.com/a/70209661
# Posted by Karl Knechtel
# Retrieved 2026-09-23, License - CC BY-SA 4.0
def swap_words(s, x, y):
    return y.join(part.replace(y, x) for part in s.split(x))

print("Hello, my name is ELIZA. How are you feeling today?")
chat = True
while chat == True:
    list1 = [1, 2, 3]
    random1 =  random.choice(list1)
    feel = "feel"
    end = "end"
    my = "my"
    reply = input("Reply with a sentence like the example: 'I feel happy', or with 'end' to finish this session: ")
    words = reply.split()
    if feel in words:
        print("Why do you feel " + words[2] + "?")
    else:
        match random1:
            case 1: print("Go on.")
            case 2: print("Keep going.")
            case 3: print("Tell me more about that.")
    if end in words:
        chat = False
print("Thank you for this session.")
