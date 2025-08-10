from Backend import AiAPi
from Backend.SwitchModels import SwitchModels


class Node:
    def __init__(self, x):
        self.data = x
        self.next = None


class ResponseHistory:

    def __init__(self, lst=None):
        self.model_loader = AiAPi.ModelLoader()
        self.switch_model = SwitchModels()
        self.current = None
        self.head = None
        self.tail = None

    def insert_response(self, response):
        data = self.get_ai_response(response)
        new_node = Node(data)

        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        elif self.current is None:
            self.tail.next = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.current.next = new_node
            self.tail = new_node
            self.current = new_node

        print(f"Inserted new response: {data}")
        return data  # RETURN IT!

    def show_previous_response(self):
        if not self.head:
            print("No conversations found.")
            return None

        if self.current is None:
            # Start from tail if no current yet
            self.current = self.tail
            print(f"Showing: {self.current.data}")
            return self.current.data

        # If already at head, can't go further back
        if self.current == self.head:
            print("Already at oldest response.")
            return self.current.data

        # Otherwise, find the previous node
        temp = self.head
        prev = None
        while temp and temp != self.current:
            prev = temp
            temp = temp.next

        if prev:
            self.current = prev
            print(f"Showing: {self.current.data}")
            return self.current.data
        else:
            print("No previous node found.")
            return None

    def show_next_response(self):
        if not self.head:
            print("No conversations found.")
            return None

        if self.current is None:
            # Start from head if no current yet
            self.current = self.head
            print(f"Showing: {self.current.data}")
            return self.current.data

        if self.current.next:
            self.current = self.current.next
            print(f"Showing: {self.current.data}")
            return self.current.data
        else:
            print("Already at newest response.")
            return self.current.data

    def get_ai_response(self, proof: str) -> str:
        if self.switch_model.model == "gpt-4o":
            return self.model_loader.load_model_openai(proof)
        elif self.switch_model.model == "gemini":
            return self.model_loader.load_model_google_gemini(proof)
        else:
            raise ValueError("Invalid model selected.")
