import streamlit as st
from pawpal_system import Pet, Owner, CareTask, DailyPlanner

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Check if the DailyPlanner is already in the "vault". If not, create a default one.
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
    # Update owner details directly in the session state object
    new_owner_name = st.text_input("Owner name", value=planner.owner.name)
    new_time = st.number_input("Available time today (mins)", min_value=0, max_value=720, value=planner.owner.available_time)
    
    planner.owner.name = new_owner_name
    planner.owner.update_available_time(new_time)

with col_pet:
    # Update pet details
    new_pet_name = st.text_input("Pet name", value=planner.owner.pet.name)
    new_species = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(planner.owner.pet.species))
    new_age = st.number_input("Pet age", min_value=0, max_value=30, value=planner.owner.pet.age)
    
    # Update the existing pet's attributes directly
    planner.owner.pet.name = new_pet_name
    planner.owner.pet.species = new_species
    planner.owner.pet.age = new_age

st.caption(f"**Current Profile:** {planner.owner.name} caring for {planner.owner.pet.get_details()} with {planner.owner.available_time} mins available.")

st.divider()

# --- ADDING TASKS ---
st.subheader("Manage Tasks")
st.caption("Add tasks to your master list. The planner will figure out what fits!")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["high", "medium", "low"], index=0)

# Map string priorities to integers (1 = High, 2 = Medium, 3 = Low)
priority_map = {"high": 1, "medium": 2, "low": 3}

if st.button("Add task"):
    # Create the CareTask using the imported class
    new_task = CareTask(
        name=task_title, 
        duration=int(duration), 
        priority=priority_map[priority_str]
    )
    # Add it to the planner
    planner.add_task(new_task)
    st.success(f"Added '{task_title}' to the task list!")

# Display current tasks using the objects stored in the planner
if planner.all_tasks:
    st.write("**Current Master List:**")
    # Convert task objects into a format Streamlit's table can easily read
    task_data = [{"Task": t.name, "Duration (mins)": t.duration, "Priority Level": t.priority} for t in planner.all_tasks]
    st.table(task_data)
else:
    st.info("No tasks added yet. Add one above.")

st.divider()

# --- GENERATE SCHEDULE ---
st.subheader("Today's Plan")

if st.button("Generate schedule"):
    if not planner.all_tasks:
        st.warning("Please add some tasks first!")
    else:
        # Run the backend logic
        planner.generate_plan()
        
        st.success("Plan generated successfully!")
        
        # Display Scheduled Tasks
        st.markdown("### ✅ Scheduled Tasks")
        if planner.scheduled_tasks:
            for t in planner.scheduled_tasks:
                st.write(f"- **{t.name}** ({t.duration} mins) - *Priority {t.priority}*")
        else:
            st.write("No tasks could fit in the schedule.")
            
        # Display Skipped Tasks
        st.markdown("### ❌ Skipped Tasks")
        if planner.skipped_tasks:
            for t in planner.skipped_tasks:
                st.write(f"- **{t.name}** ({t.duration} mins) - *Priority {t.priority}*")
        else:
            st.write("None! All tasks fit perfectly.")
            
        # Display Reasoning
        st.markdown("### 🧠 Planner Reasoning")
        st.info(planner.get_explanation())