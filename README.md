# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

PawPal+ has been upgraded with intelligent algorithms to better manage your pet's routine. The app now supports chronological sorting by time, filtering tasks by pet or completion status, and automatically rolling over recurring daily or weekly tasks. It also features a lightweight conflict detection system that warns you if overlapping tasks are scheduled for the exact same time.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

PawPal+ includes an automated test suite built with `pytest`. You can run the entire test suite from your terminal using the following command:

```bash
python -m pytest

```

**What the tests cover:**

* **Time Constraints & Priority:** Verifies that higher-priority tasks are scheduled first, and that tasks are correctly skipped if they exceed the owner's total available time.
* **Sorting Correctness:** Ensures that tasks are accurately sorted chronologically based on their `HH:MM` start times.
* **Recurrence Logic:** Confirms that marking a "daily" or "weekly" task as complete automatically generates a new, fresh task for the next occurrence.
* **Conflict Detection:** Validates that the system correctly identifies and flags warnings when multiple tasks are scheduled for the exact same time slot.

## Features

* **Chronological Sorting:** Automatically sorts scheduled tasks and the daily itinerary chronologically based on `HH:MM` start times.
* **Conflict Detection:** Identifies and warns the user if multiple care tasks are scheduled for the exact same time slot, specifying which pets are affected.
* **Automated Recurrence:** Seamlessly rolls over "daily" or "weekly" tasks by generating a new, incomplete task for the next due date when the current one is marked complete.
* **Smart Filtering:** Allows users to filter their master task list dynamically by completion status or by a specific pet's name. 
* **Priority-Based Scheduling:** Intelligently fits the highest-priority tasks into the owner's available time constraints, skipping lower-priority tasks that exceed the time limit.

## 📸 Demo
<a href="/demo_screenshot.png" target="_blank">
  <img src='/demo_screensho.png' title='PawPal App' width='' alt='PawPal App' class='center-block' />
</a>.
