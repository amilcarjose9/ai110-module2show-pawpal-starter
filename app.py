import streamlit as st
from pawpal_system import Pet, Owner, CareTask, DailyPlanner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- INITIALIZE SESSION STATE ---
if "planner" not in st.session_state:
    default_pet = Pet("Mochi", "dog", 3)
    default_owner = Owner("Jordan", 60, default_pet) # Default 60 mins available
    st.session_state.planner = DailyPlanner(default_owner)

planner = st.session_state.planner

st.markdown("Welcome to the PawPal+ app. Let's plan your pet's day!")

st.divider()

# --- OWNER & PET PROFILE ---
st.subheader("Profile Settings")

col_owner, col_pet = st.columns(2)

with col_owner:
  new_owner_name = st.text_input("Owner name", value=planner.owner.name)
  new_time = st.number_input("Available time today (mins)", min_value=0, max_value=720, value=planner.owner.available_time)
  
  planner.owner.name = new_owner_name
  planner.owner.update_available_time(new_time)

with col_pet:
  new_pet_name = st.text_input("Pet name", value=planner.owner.pet.name)
  new_species = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(planner.owner.pet.species))
  new_age = st.number_input("Pet age", min_value=0, max_value=30, value=planner.owner.pet.age)
  
  planner.owner.pet.name = new_pet_name
  planner.owner.pet.species = new_species
  planner.owner.pet.age = new_age

st.caption(f"**Current Profile:** {planner.owner.name} caring for {planner.owner.pet.get_details()} with {planner.owner.available_time} mins available.")

st.divider()

# --- ADDING TASKS ---
st.subheader("Manage Tasks")
st.caption("Add tasks to your master list. The planner will figure out what fits!")

col1, col2 = st.columns(2)
with col1:
  task_title = st.text_input("Task title", value="Morning walk")
  start_time = st.text_input("Start Time (HH:MM)", value="08:00")
  task_pet = st.text_input("For Pet (Name)", value=planner.owner.pet.name)
with col2:
  duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
  priority_str = st.selectbox("Priority", ["high", "medium", "low"], index=0)
  frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

priority_map = {"high": 1, "medium": 2, "low": 3}

if st.button("Add task"):
  new_task = CareTask(
    name=task_title, 
    duration=int(duration), 
    priority=priority_map[priority_str],
    start_time=start_time,
    frequency=frequency,
    pet_name=task_pet
  )
  planner.add_task(new_task)
  st.success(f"Added '{task_title}' at {start_time} for {task_pet}!")

st.markdown("---")

# --- MASTER LIST & FILTERING ---
st.write("**Current Master List**")

filter_col1, filter_col2 = st.columns(2)
with filter_col1:
  status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Completed"])
with filter_col2:
  pet_filter = st.text_input("Filter by Pet Name (Leave blank for all)")

# Apply the filter_tasks logic
status_map = {"All": None, "Pending": False, "Completed": True}
pet_arg = pet_filter if pet_filter.strip() != "" else None

filtered_tasks = planner.filter_tasks(status=status_map[status_filter], pet_name=pet_arg)

if filtered_tasks:
  # Use sort_by_time to make the table chronological
  sorted_filtered = sorted(filtered_tasks, key=lambda t: t.start_time)
  
  task_data = [{
    "Time": t.start_time,
    "Task": t.name, 
    "Pet": t.pet_name,
    "Duration": f"{t.duration} m", 
    "Pri.": t.priority,
    "Freq.": t.frequency.capitalize(),
    "Status": "✅ Done" if t.is_completed else "⏳ Pending"
  } for t in sorted_filtered]
  
  st.table(task_data)
else:
  st.info("No tasks match your filter criteria.")

# --- TASK COMPLETION & RECURRENCE ---
with st.expander("✅ Mark Tasks Complete"):
  pending_tasks = [t for t in planner.all_tasks if not t.is_completed]
  if pending_tasks:
    for t in pending_tasks:
      # Layout a row for each task
      c1, c2 = st.columns([4, 1])
      c1.write(f"**[{t.start_time}] {t.name}** for {t.pet_name} ({t.frequency})")

      if c2.button("Complete", key=f"comp_{id(t)}"):
        planner.mark_task_complete(t)
        st.rerun() # Refresh the UI
  else:
    st.write("No pending tasks to complete.")

st.divider()

# --- GENERATE SCHEDULE & CONFLICTS ---
st.subheader("Today's Plan")

if st.button("Generate schedule"):
  if not planner.all_tasks:
    st.warning("Please add some tasks first!")
  else:
    # Detect and warn about conflicts before showing the plan
    warnings = planner.detect_conflicts()
    if warnings:
      for w in warnings:
        st.warning(w)
    else:
      st.success("✅ No scheduling conflicts detected!")

    # Run the backend scheduling algorithm
    planner.generate_plan()
    
    # Display Scheduled Tasks (Sorted chronologically)
    st.markdown("### 🗓️ Scheduled Itinerary")
    if planner.scheduled_tasks:
      chrono_schedule = sorted(planner.scheduled_tasks, key=lambda t: t.start_time)
      for t in chrono_schedule:
        st.write(f"- **[{t.start_time}] {t.name}** (for {t.pet_name}) • *{t.duration} mins, Priority {t.priority}*")
    else:
      st.write("No tasks could fit in the schedule.")
        
    # Display Skipped Tasks
    st.markdown("### ❌ Skipped Tasks")
    if planner.skipped_tasks:
      for t in planner.skipped_tasks:
        st.write(f"- **[{t.start_time}] {t.name}** (for {t.pet_name}) • *{t.duration} mins, Priority {t.priority}*")
    else:
      st.write("None! All tasks fit perfectly.")
        
    # Display Reasoning
    st.markdown("### 🧠 Planner Reasoning")
    st.info(planner.get_explanation())
