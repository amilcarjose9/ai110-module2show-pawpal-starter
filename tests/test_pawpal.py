from datetime import timedelta
from pawpal_system import Pet, Owner, CareTask, DailyPlanner

def test_time_constraint_skips_tasks():
  """Test that the planner skips tasks if they exceed the owner's available time."""
  # Setup
  pet = Pet("Buddy", "Dog", 3)
  owner = Owner("Alex", available_time=30, pet=pet) # Only 30 minutes available
  planner = DailyPlanner(owner)
  
  # Create two tasks that total 40 minutes
  task1 = CareTask("Walk", duration=20, priority=1)
  task2 = CareTask("Play", duration=20, priority=1)
  
  planner.add_task(task1)
  planner.add_task(task2)
  
  # Action
  planner.generate_plan()
  
  # Assertions
  assert len(planner.scheduled_tasks) == 1, "Only one 20-minute task should fit."
  assert len(planner.skipped_tasks) == 1, "The second task should be skipped due to lack of time."


def test_priority_sorting():
  """Test that higher priority tasks (lower number) are scheduled first."""
  # Setup
  pet = Pet("Luna", "Cat", 5)
  owner = Owner("Sam", available_time=45, pet=pet) # 45 minutes available
  planner = DailyPlanner(owner)
  
  # Create a lower priority task (added first) and a higher priority task (added second)
  low_priority_task = CareTask("Grooming", duration=30, priority=3)
  high_priority_task = CareTask("Give Meds", duration=20, priority=1)
  
  # Add them out of order to ensure the algorithm actually sorts them
  planner.add_task(low_priority_task)
  planner.add_task(high_priority_task)
  
  # Action
  planner.generate_plan()
  
  # Assertions
  assert len(planner.scheduled_tasks) == 1, "Only one task can fit into 45 mins since 30+20=50."
  assert planner.scheduled_tasks[0].name == "Give Meds", "The higher priority task must be scheduled first."
  assert planner.skipped_tasks[0].name == "Grooming", "The lower priority task should be skipped."


def test_sorting_by_time():
  """Verify tasks are returned in chronological order based on start_time."""
  owner = Owner("Alex", available_time=60, pet=Pet("Buddy", "Dog", 3))
  planner = DailyPlanner(owner)
  
  # Add tasks out of chronological order
  task1 = CareTask("Lunch", duration=10, priority=1, start_time="12:00")
  task2 = CareTask("Breakfast", duration=10, priority=1, start_time="08:00")
  task3 = CareTask("Dinner", duration=10, priority=1, start_time="18:00")
  
  planner.add_task(task1)
  planner.add_task(task2)
  planner.add_task(task3)
  
  sorted_tasks = planner.sort_by_time()
  
  # Check that they sorted correctly
  assert sorted_tasks[0].name == "Breakfast"
  assert sorted_tasks[1].name == "Lunch"
  assert sorted_tasks[2].name == "Dinner"


def test_recurrence_logic():
  """Confirm that marking a daily task complete creates a new task for the following day."""
  owner = Owner("Alex", available_time=60, pet=Pet("Buddy", "Dog", 3))
  planner = DailyPlanner(owner)
  
  # Create a daily task
  daily_task = CareTask("Morning Walk", duration=20, priority=1, frequency="daily")
  planner.add_task(daily_task)
  original_due_date = daily_task.due_date
  
  # Action: Mark it complete
  planner.mark_task_complete(daily_task)
  
  # Assertions
  assert daily_task.is_completed is True, "The original task should be marked complete."
  assert len(planner.all_tasks) == 2, "A new recurring task should have been added to the master list."
  
  new_task = planner.all_tasks[1]
  assert new_task.name == "Morning Walk", "The new task should have the same name."
  assert new_task.is_completed is False, "The newly generated task should NOT be complete."
  assert new_task.due_date == original_due_date + timedelta(days=1), "The due date should be exactly 1 day in the future."


def test_conflict_detection():
  """Verify that the Scheduler flags duplicate times."""
  owner = Owner("Alex", available_time=60, pet=Pet("Buddy", "Dog", 3))
  planner = DailyPlanner(owner)
  
  # Create two tasks at the exact same time
  task1 = CareTask("Walk Buddy", duration=20, priority=1, start_time="08:00", pet_name="Buddy")
  task2 = CareTask("Feed Luna", duration=10, priority=1, start_time="08:00", pet_name="Luna")
  
  # Create a third task at a safe time
  task3 = CareTask("Groom Buddy", duration=30, priority=2, start_time="10:00", pet_name="Buddy")
  
  planner.add_task(task1)
  planner.add_task(task2)
  planner.add_task(task3)
  
  warnings = planner.detect_conflicts()
  
  # There should only be ONE conflict warning (for the 08:00 slot)
  assert len(warnings) == 1, "There should be exactly one conflict detected."
  
  # The warning should mention the time and the conflicting tasks
  assert "08:00" in warnings[0]
  assert "Walk Buddy" in warnings[0]
  assert "Feed Luna" in warnings[0]
