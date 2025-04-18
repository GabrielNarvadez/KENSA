import json

class UndoRedoStack:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def perform_action(self, action):
        self.undo_stack.append(action)
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            action = self.undo_stack.pop()
            self.redo_stack.append(action)
            return action
        return None

    def redo(self):
        if self.redo_stack:
            action = self.redo_stack.pop()
            self.undo_stack.append(action)
            return action
        return None

# Example Input
def handle_undo_redo(request_json):
    data = json.loads(request_json)
    stack = UndoRedoStack()
    
    for action in data.get("actions", []):
        stack.perform_action(action)
    
    if data.get("command") == "undo":
        undone_action = stack.undo()
        return json.dumps({"status": "undone", "action": undone_action})
    elif data.get("command") == "redo":
        redone_action = stack.redo()
        return json.dumps({"status": "redone", "action": redone_action})

# Example Usage
request_json = json.dumps({
    "actions": ["Edit Profile", "Change Email"],
    "command": "undo"
})
print(handle_undo_redo(request_json))
