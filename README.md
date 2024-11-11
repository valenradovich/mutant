# mutant detection
base url: https://mutant-detector.bluehill-82a8baaa.eastus.azurecontainerapps.io/

## examples of API testing with curl

- checking if the DNA is mutant

```bash
curl -X POST "https://mutant-detector.bluehill-82a8baaa.eastus.azurecontainerapps.io/mutant/" \
-H "Content-Type: application/json" \
-d '{
    "dna": [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
    ]
}'
```

- checking if the DNA is not mutant

```bash
curl -X POST "https://mutant-detector.bluehill-82a8baaa.eastus.azurecontainerapps.io/mutant/" \
-H "Content-Type: application/json" \
-d '{
    "dna": [
        "ATGCGA",
        "CAGTGC",
        "TTATTT",
        "AGACGG",
        "GCGTCA",
        "TCACTG"
    ]
}'
```


- checking if the DNA is not valid

```bash
curl -X POST "https://mutant-detector.bluehill-82a8baaa.eastus.azurecontainerapps.io/mutant/" \
-H "Content-Type: application/json" \
-d '{
    "dna": [
        "ATG",
        "CAG",
        "TTA"
    ]
}'
```

- checking statistics

```bash
curl -X GET "https://mutant-detector.bluehill-82a8baaa.eastus.azurecontainerapps.io/stats/"
```

## examples of API testing with python
you can run the test.py file inside the tests folder
```bash
python tests/test.py
```






