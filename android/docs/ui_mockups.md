# Kairix Todo Android App UI Mockups

## Overview

This document provides detailed UI mockups for the Kairix Todo Android app, which will integrate with the existing Kairix Todo web service. The app follows Material Design 3 principles and provides a clean, intuitive interface for managing tasks.

## Color Scheme

```
Primary: #1976D2 (Blue 700)
Secondary: #03DAC6 (Teal A400)
Background: #F5F5F5 (Grey 100)
Surface: #FFFFFF (White)
Error: #B00020 (Red)
Text Primary: #212121 (Grey 900)
Text Secondary: #757575 (Grey 600)
```

## Typography

```
Headings: Roboto Medium
Body: Roboto Regular
Button Text: Roboto Medium
```

## Screen Mockups

### 1. Main Task List Screen

```
┌─────────────────────────────────────────┐
│ ≡ Kairix Todo                      🔍 ⋮ │ <- App bar with menu, title, search, options
├─────────────────────────────────────────┤
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ☐ Buy groceries                   > │ │ <- Task item with checkbox and chevron
│ │   #shopping #errands               │ │ <- Tags
│ │   Today                            │ │ <- Due date
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ☐ Finish project report           > │ │
│ │   #work                            │ │
│ │   Tomorrow                         │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ☑ Call dentist                    > │ │ <- Completed task (strikethrough)
│ │   #health                          │ │
│ │   Yesterday                        │ │
│ └─────────────────────────────────────┘ │
│                                         │
│                                         │
│                  ⊕                      │ <- FAB for adding new task
│                                         │
├─────────────────────────────────────────┤
│ All | Today | Tomorrow | This Week      │ <- Bottom navigation tabs
└─────────────────────────────────────────┘
```

### 2. Task Creation/Edit Screen

```
┌─────────────────────────────────────────┐
│ ← New Task                     Save     │ <- App bar with back button and save action
├─────────────────────────────────────────┤
│                                         │
│ Title                                   │
│ ┌─────────────────────────────────────┐ │
│ │ Enter task title                    │ │ <- Title input field
│ └─────────────────────────────────────┘ │
│                                         │
│ Details (optional)                      │
│ ┌─────────────────────────────────────┐ │
│ │ Add additional details              │ │ <- Details input field (multiline)
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Due Date                                │
│ ┌─────────────────────────────────────┐ │
│ │ Select date                      📅 │ │ <- Date picker
│ └─────────────────────────────────────┘ │
│                                         │
│ Tags                                    │
│ ┌─────────────────────────────────────┐ │
│ │ Add tags                          + │ │ <- Tag input with add button
│ └─────────────────────────────────────┘ │
│ #work #meeting                          │ <- Selected tags with remove option
│                                         │
│ Reminder                                │
│ ┌─────────────────────────────────────┐ │
│ │ Set reminder                      🔔 │ │ <- Reminder setting
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 🎤 Voice Input                      │ │ <- Voice input button
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📋 Bulk Entry                       │ │ <- Bulk entry button
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### 3. Voice Input Dialog

```
┌─────────────────────────────────────────┐
│             Voice Input                 │
├─────────────────────────────────────────┤
│                                         │
│               🎤                        │ <- Microphone icon
│                                         │
│         [Audio Visualization]           │ <- Waveform visualization
│                                         │
│ "Buy milk and eggs tomorrow"            │ <- Transcription preview
│                                         │
│                                         │
│     Cancel               Confirm        │ <- Action buttons
│                                         │
└─────────────────────────────────────────┘
```

### 4. Bulk Entry Dialog

```
┌─────────────────────────────────────────┐
│             Bulk Entry                  │
├─────────────────────────────────────────┤
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ - Buy milk                          │ │
│ │ - Schedule dentist appointment      │ │ <- Multiline text input
│ │ - Call mom                          │ │
│ │ - Finish project report             │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Preview:                                │
│ • Buy milk                              │
│ • Schedule dentist appointment          │ <- Parsed tasks preview
│ • Call mom                              │
│ • Finish project report                 │
│                                         │
│     Cancel               Add Tasks      │ <- Action buttons
│                                         │
└─────────────────────────────────────────┘
```

### 5. Task Detail View

```
┌─────────────────────────────────────────┐
│ ← Task Detail                    Edit   │ <- App bar with back button and edit action
├─────────────────────────────────────────┤
│                                         │
│ Buy groceries                           │ <- Task title
│                                         │
│ Details:                                │
│ Milk, eggs, bread, and vegetables       │ <- Task details
│                                         │
│ Due: Today (Apr 18, 2025)               │ <- Due date
│                                         │
│ Tags: #shopping #errands                │ <- Tags
│                                         │
│ Reminders:                              │
│ • Today, 5:00 PM                        │ <- Reminders list
│                                         │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ✓ Mark Complete                     │ │ <- Complete button
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 🗑️ Delete                           │ │ <- Delete button
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ 📋 Copy to Clipboard                │ │ <- Copy button
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### 6. Filter/Search View

```
┌─────────────────────────────────────────┐
│ ← Filters                      Apply    │ <- App bar with back button and apply action
├─────────────────────────────────────────┤
│                                         │
│ Search                                  │
│ ┌─────────────────────────────────────┐ │
│ │ Search tasks...                  🔍 │ │ <- Search input
│ └─────────────────────────────────────┘ │
│                                         │
│ Date Range                              │
│ ┌─────────────────────────────────────┐ │
│ │ From: [Select date]              📅 │ │ <- From date picker
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ To: [Select date]                📅 │ │ <- To date picker
│ └─────────────────────────────────────┘ │
│                                         │
│ Status                                  │
│ ○ All                                   │
│ ○ Completed                             │ <- Status radio buttons
│ ○ Incomplete                            │
│                                         │
│ Tags                                    │
│ ☑ work                                  │
│ ☐ home                                  │ <- Tag checkboxes
│ ☑ health                                │
│ ☐ shopping                              │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Reset Filters                       │ │ <- Reset button
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### 7. Settings Screen

```
┌─────────────────────────────────────────┐
│ ← Settings                              │ <- App bar with back button
├─────────────────────────────────────────┤
│                                         │
│ General                                 │
│ ┌─────────────────────────────────────┐ │
│ │ Default View                      > │ │ <- Default view setting
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ Theme                             > │ │ <- Theme setting
│ └─────────────────────────────────────┘ │
│                                         │
│ Notifications                           │
│ ┌─────────────────────────────────────┐ │
│ │ Enable Notifications       [Toggle] │ │ <- Notifications toggle
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ Reminder Sound                    > │ │ <- Reminder sound setting
│ └─────────────────────────────────────┘ │
│                                         │
│ Voice Input                             │
│ ┌─────────────────────────────────────┐ │
│ │ Language                          > │ │ <- Voice language setting
│ └─────────────────────────────────────┘ │
│                                         │
│ API Settings                            │
│ ┌─────────────────────────────────────┐ │
│ │ API URL                           > │ │ <- API URL setting
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ API Key                           > │ │ <- API key setting
│ └─────────────────────────────────────┘ │
│                                         │
│ About                                   │
│ ┌─────────────────────────────────────┐ │
│ │ Version 1.0.0                       │ │ <- App version
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

## Interactive Elements

### Task Item Swipe Actions

```
┌─────────────────────────────────────────┐
│                                         │
│ ┌─────────────────┐ ┌─────────────────┐ │
│ │                 │ │ Buy groceries   │ │ <- Left swipe reveals complete action
│ │ ✓ Complete      │ │ #shopping       │ │
│ │                 │ │ Today           │ │
│ └─────────────────┘ └─────────────────┘ │
│                                         │
│ ┌─────────────────┐ ┌─────────────────┐ │
│ │ Finish project  │ │                 │ │
│ │ #work           │ │ 🗑️ Delete       │ │ <- Right swipe reveals delete action
│ │ Tomorrow        │ │                 │ │
│ └─────────────────┘ └─────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### Multi-Select Mode

```
┌─────────────────────────────────────────┐
│ 3 Selected                 Copy  Delete │ <- App bar in multi-select mode
├─────────────────────────────────────────┤
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ☑ Buy groceries                   > │ │ <- Selected task
│ │   #shopping #errands               │ │
│ │   Today                            │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ☑ Finish project report           > │ │ <- Selected task
│ │   #work                            │ │
│ │   Tomorrow                         │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ ☑ Call dentist                    > │ │ <- Selected task
│ │   #health                          │ │
│ │   Yesterday                        │ │
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### Copy to Clipboard Dialog

```
┌─────────────────────────────────────────┐
│          Copy to Clipboard              │
├─────────────────────────────────────────┤
│                                         │
│ Format:                                 │
│ ○ Plain Text                            │
│ ● Markdown                              │ <- Format options
│ ○ HTML                                  │
│                                         │
│ Preview:                                │
│ - Buy groceries (Today)                 │
│ - Finish project report (Tomorrow)      │ <- Preview of formatted text
│ - Call dentist (Yesterday)              │
│                                         │
│     Cancel                Copy          │ <- Action buttons
│                                         │
└─────────────────────────────────────────┘
```

## Responsive Design

The app will adapt to different screen sizes and orientations:

- On larger screens (tablets), the task list and detail view can be shown side by side in a master-detail layout
- In landscape orientation, the bottom navigation may move to the side
- All input fields and touch targets will follow Android accessibility guidelines for minimum size

## Animations and Transitions

- Smooth transitions between screens using Material motion patterns
- Subtle animations for completing tasks (checkbox animation, strikethrough effect)
- Microphone visualization during voice recording
- Ripple effects on buttons and interactive elements

## Accessibility Features

- Support for screen readers
- Adjustable text sizes
- High contrast mode
- Voice commands for common actions
