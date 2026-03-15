from typing import List

class Pet:
  def __init__(self, name: str, species: str, age: int):
    self.name = name
    self.species = species
    self.age = age

  def get_details(self) -> str:
    pass


class Owner:
  def __init__(self, name: str, available_time: int, pet: Pet):
    self.name = name
    self.available_time = available_time
    self.pet = pet

  def update_available_time(self, minutes: int) -> None:
    pass


class CareTask:
  def __init__(self, name: str, duration: int, priority: int, category: str = ""):
    self.name = name
    self.duration = duration
    self.priority = priority
    self.category = category

  def update_task(self, duration: int, priority: int) -> None:
    pass


class DailyPlanner:
  def __init__(self, owner: Owner):
    self.owner = owner
    self.all_tasks: List[CareTask] = []
    self.scheduled_tasks: List[CareTask] = []
    self.skipped_tasks: List[CareTask] = []
    self.reasoning: str = ""

  def add_task(self, task: CareTask) -> None:
    pass

  def remove_task(self, task: CareTask) -> None:
    pass

  def generate_plan(self) -> None:
    pass

  def get_explanation(self) -> str:
    pass
