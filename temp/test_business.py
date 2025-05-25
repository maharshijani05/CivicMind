from business import get_business_response

policy = "The government will implement a ₹100 congestion tax for entering the city center on weekdays."

response = get_business_response(policy)
print("BusinessBot says:\n", response)
