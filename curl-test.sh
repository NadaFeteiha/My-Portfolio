!#/bin/bash

# Base URL 
API_URL="http://localhost:5000/api/timeline_post"

echo "================================================"
echo "Testing GET request"
echo "Response:"
curl -X GET $API_URL

echo "================================================"
echo -e "Testing POST request"
echo "Response:"
curl -X POST $API_URL -d 'name=nada&email=nada.feteiha@gmail.com&content=Testing endpoint.'