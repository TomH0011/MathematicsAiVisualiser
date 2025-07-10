from Backend import AiAPi


class Node:
    def __init__(self, x):
        self.data = x
        self.next = None

class ResponseHistory:

    def __init__(self, lst=None):
        self.model_loader = AiAPi.ModelLoader()

        self.head = None
        self.tail = None

        if lst:
            temp = lst.head
            while temp:
                new_node = Node(temp.data)
                if not self.head:
                    self.head = new_node
                    self.tail = new_node
                else:
                    self.tail.next = new_node
                    self.tail = new_node
                temp = temp.next

    def insert_response(self, response):
        # Pretend on click right now



    def show_previous_response(self):



    def delete_latest_response(self):
