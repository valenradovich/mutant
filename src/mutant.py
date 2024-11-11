def is_mutant(dna: list[str]) -> bool:
    n = len(dna)
    sequence_count = 0
    
    # checking horizontal and vertical sequences at the same time
    for i in range(n):
        for j in range(n-3):  # only needed to check up to n-3 bc we are looking for 4 consecutive letters
            # horizontal
            if dna[i][j] == dna[i][j+1] == dna[i][j+2] == dna[i][j+3]:
                sequence_count += 1
            # vertical
            if dna[j][i] == dna[j+1][i] == dna[j+2][i] == dna[j+3][i]:
                sequence_count += 1
            if sequence_count > 1:
                return True

    # checking diagonals:
    # down-right
    for i in range(n-3):
        for j in range(n-3):
            if dna[i][j] == dna[i+1][j+1] == dna[i+2][j+2] == dna[i+3][j+3]:
                sequence_count += 1
                if sequence_count > 1:
                    return True

    # up-right
    for i in range(3, n):
        for j in range(n-3):
            if dna[i][j] == dna[i-1][j+1] == dna[i-2][j+2] == dna[i-3][j+3]:
                sequence_count += 1
                if sequence_count > 1:
                    return True

    return False
