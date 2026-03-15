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
