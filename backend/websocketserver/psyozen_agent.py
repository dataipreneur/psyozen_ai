from tools import summary_chain, response_chain, question_chain, recommendation_chain


# llm agent

# Process function

def process_input(state, input, emotions):
    # Generate summary
    summary = summary_chain.run(current_summary=state['summary'], prompt=state['last_response'], text=input, emotion = str(emotions))
    # Generate response
    response = response_chain.run(current_summary=summary, text=input, emotion = str(emotions))
    # Generate question if needed
    if not response.endswith('?'):
        question = question_chain.run(text=input, response=response, emotion = str(emotions))
        response += ' ' + question

    # Update state
    state['summary'] = summary
    state['last_response'] = response
    state['conversation'].append({"role": "user", "content": input})
    state['conversation'].append({"role": "assistant", "content": response})

    return state, response

#Llm agent
#Condition function

# Modify the 'should_continue' function to set the 'next_step'
def should_continue(state):
    if len(state['conversation']) < 6:
        return "process_input"
    else:
        return "generate_recommendation"

#llm agent
#Generate recommendations

def generate_recommendation(state):
    user_convo_list = []
    assistant_convo_list = []

    for message in state['conversation']:
        if message['role'] == 'user':
            user_convo_list.append(message['content'])
        elif message['role'] == 'assistant':
            assistant_convo_list.append(message['content'])




    recommendation = recommendation_chain.run(user=user_convo_list, assistant=assistant_convo_list)


    state['conversation'].append({"role": "user", "content": "Generate Recommendation"})
    state['conversation'].append({"role": "assistant", "content": recommendation})
    return state, recommendation

