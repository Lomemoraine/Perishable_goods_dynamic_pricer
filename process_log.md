## Process Outline on the Implementation
## Hour-by-Hour Timeline
- **First Hour** Read through the instructions carefully,picture the actual market scenario,with the help of copilot ,break down the task into modules(Dataset generation(`generator.py`)),implement the dynamic pricer(`pricer.py`) and simulate (`simulation.ipynb`)
- **Second Hour(Approximately)** A small mixup from the Copilots suggestion on work flow,suggested I implement the pricer first,however the pricer couldn't be built without the data
- **Third Hour and fourth hour** Decided to build synthetic data generator  first (`generator.py`) to produce stock.csv, competitor_prices.csv, sales_history.csv and then proceeded to build the pricer using the data . Tested the pricer on the CLI with hardcoded data first.
- **Hour 5** Developed simulation loop in notebook. Ran 7-day simulation comparing my dynamic pricer vs. cost-plus and cheapest competitor baselines. Generated profit/waste/margin charts.
- **Hour 5 ** Drafted SMS price sheet artifact 

## LLM / Tool Usage
- **Copilot (Microsoft):** Used for brainstorming decay formulas, structuring simulation loop, and drafting SMS artifact.  
- **Reason:** Accelerated ideation and ensured clarity in math + business adaptation a field I am yet to interact with in terms of data science.  
- **Other tools:** Jupyter Notebook for simulation, GitHub for repo hosting.

## Sample Prompts Used
1. *"Show me a few alternative decay formulas"* → received exponential, linear, logistic, hybrid options(Chose Exponential  based based on my earlier research on food quality drops  slowly at first and then sharply near its shelf life(expiry))  
2. *"Start the implementation using the exponential decay formula"* → got draft `suggest_price()` code.  
3. *"Show me the simulation loop structure"* → received skeleton for 7-day simulation.  

### Discarded Prompt
- *Suggest the workflow of this work,gave me a mixed workflow in terms of the technical approach*.

## Hardest Decision
*Following my own workflow and assuming the suggested workflow *