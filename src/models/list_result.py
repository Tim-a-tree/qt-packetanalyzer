
class ListResult:
  def __init__(self):
    self.list_result = []

  def add_item(self, item):
    self.list_result.append(item)

  def get_list(self):
    return self.list_result

  def clear_list(self):
    self.list_result = []