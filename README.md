# Rule-Based Intelligent Agent
Agent that follows rule-based logic to find the goal and complete the mission in as few steps as possible. 
The agent can rotate 45 degrees at a time and move in each direction. Every move (rotation or step to a new position)
is considered a move. The agent has a sonar that it sends before every move in three directions, 3, 9, and 12 o'clock
relative to its current rotation. The sonar will update the agents internal database of the surrounding.The database 
will be shown as green or red squares, green for squares that free and red for squares that have obstacles.


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/nY1yhH-1TPo/0.jpg)](https://www.youtube.com/watch?v=nY1yhH-1TPo)
## How to start the project?

**1. Clone the project**

**2. Go to the project directory:**
```
cd RuleBasedAgent
```
**3. Install Anaconda (if you haven't installed on your local machine already):**
```
conda create agent-env python==3.7
```  
**4. Activate pipenv:**
```
conda activate agent-env
```
**5. Install all required modules listed in requirements.txt:**
```
conda install --file requirements.txt
```

