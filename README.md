# cis385_project notes
App functions successfully, can add customers to customer table, order and orderitems as well. Retrieves menu and extra items from database to display on menu page. Has a cart function to add multiple items to cart that tracks total cost. Did not get to figuring out how to assign unique ID numbers to entries such as CustomerID so sometimes will throw an error when adding a new random ID that already matches one found in the tables. 


# To launch:

python3 -m venv virt

source virt/Scripts/activate

python3 -m pip install -r requirements.txt

python3 app.py



