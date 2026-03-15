from pawpal_system import Pet, Owner, CareTask, DailyPlanner

def main():
    # Create two Pets
    pet1 = Pet("Buddy", "Golden Retriever", 3)
    pet2 = Pet("Luna", "Tabby Cat", 5)

    # Create an Owner
    owner = Owner("Alex", available_time=60, pet=pet1)

    # Create at Tasks with different times and priorities
    task1 = CareTask("Morning Walk", duration=30, priority=1, category="Exercise")
    task2 = CareTask("Feed Breakfast & Meds", duration=15, priority=1, category="Feeding")
    task3 = CareTask("Grooming & Brushing", duration=25, priority=3, category="Grooming")
    task4 = CareTask("Training Session", duration=10, priority=2, category="Enrichment")

    # Set up the Daily Planner and add tasks
    planner = DailyPlanner(owner)
    planner.add_task(task1)
    planner.add_task(task2)
    planner.add_task(task3)
    planner.add_task(task4)

    # Generate the schedule
    planner.generate_plan()

    # Print "Today's Schedule" to the terminal
    print("=== PawPal+ Testing Ground ===")
    print(f"Owner: {owner.name} (Time available: {owner.available_time} mins)")
    print(f"Primary Pet: {pet1.get_details()}")
    print(f"Secondary Pet: {pet2.get_details()} (Not scheduled today)\n")

    print("--- Today's Schedule ---")
    if not planner.scheduled_tasks:
      print("No tasks scheduled.")
    else:
      for task in planner.scheduled_tasks:
        print(f"✅ [Priority {task.priority}] {task.name} ({task.duration} mins)")

    print("\n--- Skipped Tasks ---")
    if not planner.skipped_tasks:
      print("None! All tasks fit.")
    else:
      for task in planner.skipped_tasks:
        print(f"❌ [Priority {task.priority}] {task.name} ({task.duration} mins)")

    print("\n--- Planner Reasoning ---")
    print(planner.get_explanation())

if __name__ == "__main__":
  main()