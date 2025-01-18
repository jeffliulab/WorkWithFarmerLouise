# WorkWithFarmerLouise

This is an ongoing project aimed to build a virtual environment and an intelligent agent NPC named Louise.

The framework:
* Intelligent Agent (Louise):
* Virtual Environment

## Demo

I have released a demo of this idea：
* Youtube: https://youtu.be/RqKZmQSIQvk?si=GH2rnMkS13hkyQzJ
* Github Codes: https://github.com/jeffliulab/A_Simple_AI_Agent/blob/main/game_demo.py

## Proposal

### 1. Project Goal
Build an open-world virtual environment where intelligent NPCs collaborate with players through dialogue. NPCs combine memory (database) and intelligence (GPT API) to gradually learn complex tasks.

---

### 2. System Architecture

1) Player Input Layer  
- **Input Methods**: Chatbox or voice commands.  
- **Functionality**: Accept player instructions, e.g., "Move two steps right" or "Build a house."

2) Intelligence Layer  
- **GPT API**:  
  - Parse player instructions and generate high-level plans.  
  - Task decomposition: Break complex goals into simple steps (e.g., "Move," "Gather," "Build").  
  - Dialogue generation: Create NPC responses based on context.

3) Memory Layer  
- **Database**:  
  - Store NPC state, task history, and skill progression.  
  - Record environment information (object locations, resources, task status).  
  - **Options**: SQLite (lightweight) or MongoDB (scalable).

4) Behavior Execution Layer  
- **Basic Actions**: Hardcoded simple actions (e.g., move, pick up, interact).  
- **Complex Actions**: Behavior Tree (BT) or Finite State Machine (FSM) for multi-step tasks.

5) Virtual World  
- **Physics Rules**: Simulate gravity, collision, etc., using Unity or Pygame.  
- **World Elements**: Dynamically generated maps with interactive objects (e.g., tools, farmland).

---

### 3. Core Features

- **Dialogue System**:  
  - Natural language communication between players and NPCs.  
  - GPT generates responses and task plans based on context.

- **Learning Ability**:  
  - NPC starts with basic abilities (e.g., movement).  
  - Gradually learns complex tasks (e.g., carrying items, collaborative building) through dialogue.

- **Task Scheduling & Execution**:  
  - Supports single and multi-task queues.  
  - Adjusts task order based on priority.

- **Dynamic Memory**:  
  - Database records task results to optimize future planning.  
  - Shared knowledge base for multi-NPC collaboration.

- **Open-World Interaction**:  
  - Dynamic world changes (e.g., day-night cycle, resource updates).  
  - NPCs interact with objects and terrain in the environment.

---

### 4. Technology Stack

- **Programming Language**: Python  
- **Game Engine**: Pygame or Unity  
- **Database**: SQLite or MongoDB  
- **AI API**: OpenAI GPT-4  
- **Additional Tools**: Flask/Django for monitoring and auxiliary features  

---

### 5. Development Steps

1. **Build Basic Framework**:  
   - Create a virtual world and NPCs using Pygame/Unity.  
   - Implement basic actions like movement and dialogue.

2. **Integrate GPT API**:  
   - Design prompt templates for instruction parsing.  
   - Implement task planning functionality.

3. **Set Up Database**:  
   - Store NPC states, task progress, and learning records.  
   - Optimize query and update processes.

4. **Expand World and Capabilities**:  
   - Add more interactive objects and mechanisms.  
   - Enhance NPC behavior complexity.
