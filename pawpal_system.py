from typing import List, Optional
from datetime import date, timedelta

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
  def __init__(
    self, 
    name: str, 
    duration: int, 
    priority: int, 
    category: str = "",
    start_time: str = "08:00", 
    frequency: str = "once",
    pet_name: str = "",
    due_date: Optional[date] = None
  ):
    """Initialize a new CareTask with scheduling and recurrence details."""
    self.name = name
    self.duration = duration
    self.priority = priority
    self.category = category
    self.start_time = start_time
    self.frequency = frequency.lower()
    self.pet_name = pet_name
    self.is_completed = False
    self.due_date = due_date if due_date else date.today()

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

  def sort_by_time(self) -> List[CareTask]:
    """Sort tasks chronologically based on their HH:MM start time string."""
    return sorted(self.all_tasks, key=lambda t: t.start_time)

  def filter_tasks(self, status: Optional[bool] = None, pet_name: Optional[str] = None) -> List[CareTask]:
    """Filter the master list by completion status and/or pet name."""
    filtered_list = self.all_tasks
    if status is not None:
      filtered_list = [t for t in filtered_list if t.is_completed == status]
    if pet_name is not None:
      filtered_list = [t for t in filtered_list if t.pet_name.lower() == pet_name.lower()]
    return filtered_list

  def mark_task_complete(self, task: CareTask) -> None:
    """Mark a task complete and generate the next occurrence if it's a recurring task."""
    if task in self.all_tasks:
      task.is_completed = True
      
      # Check for recurrence and create a new task using timedelta
      if task.frequency in ["daily", "weekly"]:
        days_to_add = 1 if task.frequency == "daily" else 7
        new_due_date = task.due_date + timedelta(days=days_to_add)
        
        new_task = CareTask(
          name=task.name,
          duration=task.duration,
          priority=task.priority,
          category=task.category,
          start_time=task.start_time,
          frequency=task.frequency,
          pet_name=task.pet_name,
          due_date=new_due_date
        )
        self.add_task(new_task)

  def detect_conflicts(self) -> List[str]:
    """Detect if multiple tasks are scheduled at the same time and return a list of warnings."""
    warnings = []
    time_slots = {}
    
    # Group tasks by their start_time
    for task in self.all_tasks:
      if not task.is_completed:  # Only check incomplete tasks
        if task.start_time not in time_slots:
          time_slots[task.start_time] = []
        time_slots[task.start_time].append(task)
                
    # Check for any time slots that have more than 1 task
    for time, tasks in time_slots.items():
      if len(tasks) > 1:
        # Build a detailed string showing the task and the pet it belongs to
        task_details = [f"'{t.name}' (for {t.pet_name or 'Unknown Pet'})" for t in tasks]
        conflict_names = " and ".join(task_details)
        
        warnings.append(f"⚠️ Conflict detected at {time}: {conflict_names}.")
            
    return warnings
  
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
      if task.is_completed:
        continue # Skip already completed tasks when planning the rest of the day
          
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
