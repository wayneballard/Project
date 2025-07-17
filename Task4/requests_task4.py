import requests

post_url = 'http://localhost/PhpProject1/Task4.php'
post_data = {
    'R': 255,
    'G':100,
    'B':0
}

post_response = requests.post(post_url, data=post_data);
print(f"POST Response:{post_response.text}")

#x, y = 3, 3
#get_url = f'http://localhost/PhpProject1/Task4.php?x={x}&y={y}'
# =  requests.get(f'http://localhost/PhpProject1/Task4.php?x={x}&y={y}')
#print(f"GET Response:{get_response.text}")