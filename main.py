from pawpal_system import Pet, Owner, CareTask, DailyPlanner

def main():
    # Create two Pets
    pet1 = Pet("Buddy", "Golden Retriever", 3)
    pet2 = Pet("Luna", "Tabby Cat", 5)

    # Create an Owner
    owner = Owner("Alex", available_time=60, pet=pet1)

    # Create Tasks with different times, priorities
    # Conflict: Both task1 and task2 are scheduled for 08:00!
    task1 = CareTask("Morning Walk", duration=30, priority=1, category="Exercise", start_time="08:00", pet_name="Buddy")
    task2 = CareTask("Feed Breakfast & Meds", duration=15, priority=1, category="Feeding", start_time="08:00", pet_name="Luna")
    
    # These tasks have unique times, so they won't conflict
    task3 = CareTask("Grooming & Brushing", duration=25, priority=3, category="Grooming", start_time="10:00", pet_name="Buddy")
    task4 = CareTask("Training Session", duration=10, priority=2, category="Enrichment", start_time="14:00", pet_name="Buddy")

    # Set up the Daily Planner and add tasks
    planner = DailyPlanner(owner)
    planner.add_task(task1)
    planner.add_task(task2)
    planner.add_task(task3)
    planner.add_task(task4)

    print("=== PawPal+ Testing Ground ===")
    print(f"Owner: {owner.name} (Time available: {owner.available_time} mins)")
    print(f"Primary Pet: {pet1.get_details()}")
    print(f"Secondary Pet: {pet2.get_details()}\n")

    # Detect conflict
    print("--- Conflict Detection ---")
    warnings = planner.detect_conflicts()
    if warnings:
        for warning in warnings:
            print(warning)
    else:
        print("✅ No scheduling conflicts detected.")
    print()

    # Generate the schedule
    planner.generate_plan()
    
    print("--- Today's Schedule ---")
    if not planner.scheduled_tasks:
      print("No tasks scheduled.")
    else:
      for task in planner.scheduled_tasks:
        print(f"✅ [{task.start_time}] [Priority {task.priority}] {task.name} ({task.duration} mins) - {task.pet_name}")

    print("\n--- Skipped Tasks ---")
    if not planner.skipped_tasks:
      print("None! All tasks fit.")
    else:
      for task in planner.skipped_tasks:
        print(f"❌ [{task.start_time}] [Priority {task.priority}] {task.name} ({task.duration} mins) - {task.pet_name}")

    print("\n--- Planner Reasoning ---")
    print(planner.get_explanation())

if __name__ == "__main__":
  main()