def simulate_vm(trace_file):
    """
    Simulates a virtual memory system based on a given address trace.
    """

    # --- Configuration ---
    NUM_FRAMES = 30
    OFFSET_BITS = 10

    # --- State Initialization ---
    total_accesses = 0
    total_hits = 0
    total_misses = 0
    total_compulsory_misses = 0
    page_frames = [None] * NUM_FRAMES
    rr_pointer = 0
    current_pid = None
    process_pages_seen = {}

    try:
        with open(trace_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue

                command = parts[0]

                if command == 'new':
                    pid = int(parts[1])
                    if pid not in process_pages_seen:
                        process_pages_seen[pid] = set()

                elif command == 'switch':
                    pid = int(parts[1])
                    current_pid = pid
                    if current_pid not in process_pages_seen:
                        process_pages_seen[current_pid] = set()

                elif command == 'access':
                    if current_pid is None:
                        continue
                    
                    total_accesses += 1
                    address = int(parts[1])
                    page_number = address >> OFFSET_BITS
                    page_to_find = (current_pid, page_number)

                    if page_to_find in page_frames:
                        total_hits += 1
                    else:
                        total_misses += 1
                        if page_number not in process_pages_seen[current_pid]:
                            total_compulsory_misses += 1
                            process_pages_seen[current_pid].add(page_number)

                        page_frames[rr_pointer] = page_to_find
                        rr_pointer = (rr_pointer + 1) % NUM_FRAMES

    except FileNotFoundError:
        print(f"Error: Trace file '{trace_file}' not found.")
        print("Please make sure 'VMInput.txt' is in the same directory.")
        return
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        return

    # --- Print Final Report ---
    print(f"Access: {total_accesses}")
    print(f"Hits: {total_hits}")
    print(f"Misses: {total_misses}")
    print(f"Compulsory Misses: {total_compulsory_misses}")


# --- Main execution ---
if __name__ == "__main__":
    INPUT_FILE = "VMInput1.txt"
    simulate_vm(INPUT_FILE)
