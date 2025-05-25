from citizen import get_citizen_response

policy = "The government will implement a ₹100 congestion tax for entering the city center on weekdays."

response = get_citizen_response(policy)
print("CitizenBot says:\n", response)
