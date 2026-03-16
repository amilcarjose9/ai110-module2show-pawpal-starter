# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

### UML Design Overview

The initial UML design models a straightforward scheduling system connecting a pet owner's available time with their pet's daily needs. It uses a central planner to evaluate a list of tasks against the owner's constraints, ultimately outputting an actionable, prioritized daily schedule.

### Classes and Responsibilities

* **`Pet`**: Holds basic demographic details about the animal receiving care (like name, species, and age) to help personalize the app experience.
* **`Owner`**: Represents the user of the app, keeping track of their name, the pet they own, and—most importantly—their total available time constraint for the day.
* **`CareTask`**: Defines a specific activity (like walking or feeding), storing critical scheduling data such as how long the task takes (duration) and how important it is (priority).
* **`DailyPlanner`**: Acts as the core logic engine of the system. It is responsible for managing the master list of tasks, running the algorithm to fit tasks into the owner's available time based on priority, and generating the final schedule along with an explanation of its choices.


**b. Design changes**

My design did not change during the initial implementation phase.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler primarily considers the owner's total available time, task priority levels, and individual task durations. I decided that task priority mattered most to ensure critical pet needs, like feeding or medication, are always scheduled first. Task duration serves as a secondary constraint to maximize the total number of tasks completed within the remaining time.

**b. Tradeoffs**

One tradeoff the scheduler makes is favoring shorter tasks over longer ones when priority levels are tied. This is a reasonable tradeoff for a busy pet owner because completing multiple smaller care activities, like a quick training session and giving treats, often provides a more balanced routine than consuming all remaining available time on a single, lengthy task.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI primarily for translating my UML designs into Python code, generating the pytest test suite, and integrating my backend logic with the Streamlit frontend. The most helpful prompts were highly specific ones that included error tracebacks or clearly stated the exact objective for a new method.

**b. Judgment and verification**

One moment where I didn't accept an AI suggestion as-is was during the conflict detection step; the AI initially wrote a warning that didn't specify which pet the conflicting tasks belonged to, which missed the core objective. I also questioned the AI when a variable appeared to be undefined in a list comprehension.

---

## 4. Testing and Verification

**a. What you tested**

I tested the time constraint limits, priority-based sorting, chronological sorting by start time, daily task recurrence, and the duplicate-time conflict detection. These tests were crucial because they verified that the core algorithms were mathematically and logically sound before introducing the complexity of the Streamlit UI.

**b. Confidence**

I am very confident that the scheduler works correctly, as my 5 automated pytest functions all pass and validate the core requirements. If I had more time, I would test edge cases like what happens if a user inputs an invalid time format like "25:00", tasks with zero duration, or how the app handles generating schedules that cross over midnight.

---

## 5. Reflection

**a. What went well**

I am most satisfied with successfully connecting the backend Python classes to the Streamlit interface. Seeing the UI dynamically update to display conflict warnings, filter tasks, and generate a chronological itinerary was very rewarding.

**b. What you would improve**

If I had another iteration, I would redesign the UI to allow users to edit existing tasks directly. I would also like to upgrade the data storage from temporary session state to a real database so the schedule persists between browser sessions.

**c. Key takeaway**

One important thing I learned is that having a clear architectural plan like a UML diagram makes collaborating with AI much more effective. I also learned the importance of paying close attention to file paths and object types when debugging, as simple oversights, like passing a string instead of an object, or editing wrong files, can cause confusing errors.
