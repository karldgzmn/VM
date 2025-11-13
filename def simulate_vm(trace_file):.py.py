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

    except FileNotFoundError:
        print(f"Error: Trace file '{trace_file}' not found.")
        print("Please make sure 'VMInput.txt' is in the same directory.")
        return
    except Exception as e:
        print(f"An error occurred during simulation: {e}")
        return
