url = 'http://localhost/PhpProject1/Task4.php';

data = "R=255&G=100&B=0"
% Don't specify 'MediaType' at all
options = weboptions();

response = webwrite(url, data, options);

disp("POST Response:");
disp(response);

