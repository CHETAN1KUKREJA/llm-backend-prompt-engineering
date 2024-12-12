from Nlp2Json import extractor_Jsonformer,extractor_RE
text = """## Step 0: Plan what to do for a short period                       
To maximize the amount of money, the first step is to gather information about the current state of the trade centre and the forest. Since there is another agent, Maria, at the trade centre, it might be beneficial to interact with her to see if there are any trade opportunit
ies. The plan is to:                                                
1. Talk to Maria to gather information about her current stock of apples and money.                                                      
2. Ask Maria if she is willing to trade apples for money.           
3. If a trade is possible, negotiate the terms of the trade.                                                                             
4. If no trade is possible with Maria, consider going to the forest to collect apples.                                                   

## Step 1: Extract a sequence of actions and parameters pairs from the plan                                                              
### Substep 1.1.1: Output description of the action                 
1. Action: talk                                                     
2. Parameters: volume, content                                      
3. list:                                                            
- Talk to Maria to gather information about her current stock of apples and money.                                                       
- Ask Maria if she is willing to trade apples for money.            

### Substep 1.1.2: Verify the action and parameters                 
1. The action "talk" appears in the plan.                           
2. The sentences covering the action and parameters appear in the plan.                                                                  
3. The parameter "content" might need to be specified based on Maria's response, which will be answered by her.                          
Considering the need to interact with Maria first, the sequence of actions starts with talking to her.                                   

## Step 2: Format the plan as function calls in JSON objects within single XML tags                                                      
Given the plan and the actions available, the first step is to talk to Maria. The function call for this action is:                      

<tool_call>                                                         
{"name": "talk", "arguments": {"volume": "normal", "content": "Hello Maria, what are you trading today?"}}                               
</tool_call>                                                        

This initial interaction is aimed at gathering information and setting the stage for potential trades or other actions based on Maria's response. Further actions will depend on her answer, which could involve negotiating a trade, deciding to go to the forest, or other option
s based on the information exchanged.                               
Finished in 162.5875s
"""
results = extractor_RE(text)
print(results)
for result in results:
    if result['json']:
        json_obj = result['json']
        print(json_obj)
    else:
        # Handle invalid JSON
        print(f"Failed to parse JSON: {result['error']}")

print("-"*20)
results = extractor_RE(text)

print(results)
for result in results:
    if result['json']:
        json_obj = result['json']
        print(json_obj)
    else:
        # Handle invalid JSON
        print(f"Failed to parse JSON: {result['error']}")

