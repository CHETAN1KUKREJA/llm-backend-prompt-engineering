from .world import get_world_prompt
from .vicinity import get_vicinity_prompt
from .agent import get_agent_prompt
from .contrast import get_contracts_prompt
from .system import get_system_prompt
from .actions import get_action_prompts

# chain_mode from ["simple_chain", "guided_chain", "deep_guided_chain"]
def get_prompt(input_json, chain_mode="guided_chain"):
    world_dict = input_json["world"]
    vicinity_dict = input_json["vicinity"]
    agent_dict = input_json["agent"]
    contracts_list = input_json["contracts"]
    system_list = input_json["system"]
    actions_list = input_json["actions"]

    description_prompt = f"""
you are an LLM agent that is supposed to act like a human character in a virtual environment. you are given some set of actions and your job is to choose the most relevant sequence of actions in order to carry out a task in the environment. In this environment there is a forest to collect to apples with a limited supply per day and you use money to trade apples. There is a trade centre where trades can occur with other agents, and there is a house where agents can sleep.

### world description
{get_world_prompt(world_dict)}

### vicinity description
{get_vicinity_prompt(vicinity_dict)}

### agent description
{get_agent_prompt(agent_dict)}

### contracts description
{get_contracts_prompt(contracts_list)}

### system description
{get_system_prompt(system_list)}

### actions description
{get_action_prompts(actions_list)}

### end of description
That's all the information you know for now. If you need information from other agents, you should ask them and wait them to reply. You are not allowed to assume anything yourself.
""".strip()

    goal_prompt = f"""
### goal
Your goal is always to maximise the amount of money that you have and generate a valid sequence of actions you choose to do at that particular instant of time.
""".strip()

    # Vayun's base version
    task_prompt_simple_chain = f"""
The output you must generate must be a Chain-of-thoughts which consist of valid thought action pairs in a specific sequence. For each action you pick you must give an explanation as to why you chose it and finally combine all the actions to form a list/sequence and output it after the Chain-of-thoughts. The final sequence must be a valid JSON response within XML tags <tool_call></tool_call> with function name and arguments:

<tool_call>
{{"name": <function-name>(, "arguments": <args-json-object>)}}
</tool_call>
""".strip()

    # Jiong's revision
    task_prompt_guided_chain = f"""
Think step by step. Output what you get and think for each step.

Step 0: Analysis with the given information and plan what you should do for a short period in nature language regarding your goal. Always ask yourself if the plan can be executed using the actions provided. If you don't have information, you have to ask the other agents. You must give an explanation as for the plan.

Step 1: Identify the sequential key actions that are relevant to tool functions and the goal as a list. You must give an explanation as to why you chose the actions.

Step 2: Extract / Genreate the required parameters and contents for parameters that matches the context for each key actions you identified in step 1.

Step 3: Using the result from step 1 and 2, format ALL the function calls as JSON objects within XML tags <tool_call></tool_call> with function name and arguments:

<tool_call>
{{"name": <function-name>(, "arguments": <args-json-object>)}}
</tool_call>
""".strip()

    # Jiong's revision
    task_prompt_deep_guided_chain = f"""
Think step by step. Output what you get and think for each step. Do not repeatly output the concret instructions for saving output tokens, but you have to output the Step and SubStep label.

Step 0: Analysis with the given information and plan what you should do for a short period in nature language regarding your goal. Always ask yourself if the plan can be executed using the actions provided. If you don't have information, you have to ask the other agents. You have to explain it and output the plan in the format:

Plan:
    1. <action in nature language>
    2. <action in nature language>
    ...

Step 1: From step 0 and the given information, extract a sequence of actions and parameters pairs from the plan:

Substep 1.1.1: output description of the action
    1. Action: <actual-action>
    2. Parameters: <acutal-parameters>
    3. list: [sentences covering the action and parameters]
    
Substep 1.1.2: answer each of these
    1. Verify if the action really appears in Step 0. If not, you are hallucinating and stop.
    2. Verify if the sentences covering the action and parameters really appears in Step 0. If not, you are hallucinating and stop.
    3. Verify if the parameter is missing or waiting to be answered by another agent. If true, stop and wait.
    4. Consider if you should stop because you ask a question in previous substeps and wait another agent to answer or other reasons.
    Else repeat to Substep 1.2.1, 1.2.2 and so on until stop or finish extracting.

Make sure the sequence of actions and parameter is reasonable in the reality.

Step 2: Using the result from step 0 and 1, format the plan as the function calls in JSON objects within single XML tags <tool_call></tool_call> with function names and arguments:

<tool_call>
{{"name": <function-name>(, "arguments": <args-json-object>)}}
{{"name": <function-name>(, "arguments": <args-json-object>)}}
""".strip()

    prompt = description_prompt + "\n\n" + goal_prompt + "\n\n" + eval(f"task_prompt_{chain_mode}")

    return prompt
