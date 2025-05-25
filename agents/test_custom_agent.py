from custom_agent import get_custom_agent_response

policy = "The government will implement a ₹100 congestion tax for entering the city center on weekdays."
prior_context=[]
persona = "Legal Advisor to the Mayor"
tone = "formal"

response = get_custom_agent_response(policy, prior_context, persona, tone)
print("CustomBot says:\n", response)