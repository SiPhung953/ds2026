import re

# Input
INPUT_DATA = [
    "The quick brown fox jumps over the lazy dog.",
    "The dog barks and the fox runs away.",
    "quick quick quick",
]

# Mapper Function
def mapper(line):
    # Takes a line of text, splits it into words, and emits (word, 1) for each
    # Convert to lowercase and remove non-word characters
    line = line.lower()
    words = re.findall(r'\b\w+\b', line)

    # Output: [('the', 1), ('quick', 1), ...]
    return [(word, 1) for word in words]

# Shuffle/Group Function
def grouper(mapped_pairs):
    # Groups the intermediate (word, 1) pairs by the word (key)
    grouped_data = {}
    for key, value in mapped_pairs:
        # Append the value (which is always 1) to the list for that key
        grouped_data.setdefault(key, []).append(value)
    # Output: {'the': [1, 1, 1], 'quick': [1, 1, 1], ...}
    return grouped_data

# Reducer Function
def reducer(word, counts):
    # Takes a word and a list of '1's, sums the list to get the total count.
    # Output: (word, total_count)
    return (word, sum(counts))

def run_word_count(data):
    # Apply the mapper to every line
    print("Map Phase")
    mapped_results = []
    for line in data:
        mapped_results.extend(mapper(line))

    print(f"Total pairs: {len(mapped_results)}")
    print(mapped_results[:5], "...") # Show the first few pairs

    # Group the pairs by key
    print("\nShuffle and Group Phase")
    grouped_results = grouper(mapped_results)

    print(f"Unique words found: {len(grouped_results)}")
    print({k: grouped_results[k][:3] for k in list(grouped_results)[:3]}, "...") # Show first 3 keys and their values

    # Apply the reducer to each word and its list of counts
    print("\nReduce Phase")
    final_results = []
    for word, counts in grouped_results.items():
        final_results.append(reducer(word, counts))

    final_output = dict(final_results)
    print("\n--- Final Word Counts ---")
    for word, count in sorted(final_output.items()):
        print(f"'{word}': {count}")

    return final_output

if __name__ == "__main__":
    run_word_count(INPUT_DATA)
