from typing import List

class Pet:
  def __init__(self, name: str, species: str, age: int):
    """Initialize a new Pet instance with basic demographic details."""
    self.name = name
    self.species = species
    self.age = age

  def get_details(self) -> str:
    """Return a formatted string containing the pet's name, species, and age."""
    return f"{self.name} the {self.species} ({self.age} years old)"


class Owner:
  def __init__(self, name: str, available_time: int, pet: Pet):
    """Initialize a new Owner instance with their available time and primary pet."""
    self.name = name
    self.available_time = available_time
    self.pet = pet

  def update_available_time(self, minutes: int) -> None:
    """Update the owner's available time, ensuring it does not drop below zero."""
    self.available_time = max(0, minutes)


class CareTask:
  def __init__(self, name: str, duration: int, priority: int, category: str = ""):
    """Initialize a new CareTask with a specific duration, priority level, and optional category."""
    self.name = name
    self.duration = duration
    self.priority = priority
    self.category = category

  def update_task(self, duration: int, priority: int) -> None:
    """Update the task's duration and priority settings."""
    self.duration = duration
    self.priority = priority


class DailyPlanner:
  def __init__(self, owner: Owner):
    """Initialize a new DailyPlanner for a specific owner and prepare empty task lists."""
    self.owner = owner
    self.all_tasks: List[CareTask] = []
    self.scheduled_tasks: List[CareTask] = []
    self.skipped_tasks: List[CareTask] = []
    self.reasoning: str = ""

  def add_task(self, task: CareTask) -> None:
    """Add a new CareTask to the planner's master list of tasks."""
    self.all_tasks.append(task)

  def remove_task(self, task: CareTask) -> None:
    """Remove a specific CareTask from the planner's master list if it exists."""
    if task in self.all_tasks:
      self.all_tasks.remove(task)

  def generate_plan(self) -> None:
    """Generate a daily schedule by fitting the highest priority tasks into the owner's available time."""
    # Reset lists and reasoning for fresh generation
    self.scheduled_tasks = []
    self.skipped_tasks = []
    self.reasoning = ""
    
    time_remaining = self.owner.available_time
    # Sort tasks: Primarily by priority (lower number = higher priority)
    # Secondarily by duration (shorter tasks first if priorities tie)
    sorted_tasks = sorted(self.all_tasks, key=lambda t: (t.priority, t.duration))

    for task in sorted_tasks:
      if task.duration <= time_remaining:
        self.scheduled_tasks.append(task)
        time_remaining -= task.duration
      else:
        self.skipped_tasks.append(task)

    # Build the reasoning explanation
    self.reasoning = f"Plan generated for {self.owner.pet.name} based on {self.owner.available_time} minutes of available time.\n"
    self.reasoning += f"Successfully scheduled {len(self.scheduled_tasks)} tasks. "
    
    if self.skipped_tasks:
      skipped_names = ", ".join([t.name for t in self.skipped_tasks])
      self.reasoning += f"\nSkipped {len(self.skipped_tasks)} tasks due to insufficient time: {skipped_names}."
    else:
      self.reasoning += "\nAll tasks were successfully fit into the schedule!"

  def get_explanation(self) -> str:
    return self.reasoning
