memory_store = {}

def update_memory(session_id, new_entry):
    memory_store.setdefault(session_id, []).append(new_entry)

def get_memory(session_id):
    return memory_store.get(session_id, [])
