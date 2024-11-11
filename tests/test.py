import requests
import time

def test_api():
    base_url = "https://mutant-detector.bluehill-82a8baaa.eastus.azurecontainerapps.io"
    
    print("Testing root endpoint:")
    print("-" * 50)
    try:
        response = requests.get(base_url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}\n")
    except Exception as e:
        print(f"Error: {str(e)}\n")

    test_cases = [
        {
            "name": "Mutant DNA (Horizontal match)",
            "dna": [
                "ATGCGA",
                "CAGTGC",
                "TTATGT",
                "AGAAGG",
                "CCCCTA",
                "TCACTG"
            ]
        },
        {
            "name": "Non-mutant DNA",
            "dna": [
                "ATGCGA",
                "CAGTGC",
                "TTATTT",
                "AGACGG",
                "GCGTCA",
                "TCACTG"
            ]
        },
        {
            "name": "Mutant DNA (Vertical match)",
            "dna": [
                "ATGCGA",
                "ATGTGC",
                "ATATGT",
                "AGAAGG",
                "CCCCTA",
                "TCACTG"
            ]
        }
    ]
    
    print("Testing /mutant/ endpoint with different sequences:")
    print("-" * 50)
    
    for test_case in test_cases:
        print(f"\nTesting {test_case['name']}:")
        try:
            response = requests.post(f"{base_url}/mutant/", json={"dna": test_case['dna']})
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Result: Mutant")
            elif response.status_code == 403:
                print("Result: Human")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        time.sleep(1)
    
    print("\nTesting /stats/ endpoint:")
    print("-" * 50)
    try:
        stats_url = f"{base_url}/stats/"
        response = requests.get(stats_url)
        if response.status_code == 200:
            stats = response.json()
            print("\nStatistics:")
            print(f"Mutants detected: {stats['count_mutant_dna']}")
            print(f"Humans detected: {stats['count_human_dna']}")
            print(f"Ratio: {stats['ratio']}")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Error accessing stats: {str(e)}")

if __name__ == "__main__":
    test_api()