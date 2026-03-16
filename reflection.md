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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
