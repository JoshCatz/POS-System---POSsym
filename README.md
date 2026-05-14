This is the database schema for our POS system!

-- Tables --
- Restaurant = metadata about the restaurant
- Employees = employees in the restaurant
- Tables = tables with metadata in restaurant
- Menu = menu with items and item data
- Order = collection of menu items
- Reservations = list of reservations for night
- Tips = server tips for payout
- Inventory = log of menu items in stock

-- Restaurant Table --
- id : serial num
- name : str
- company : str
- address : str
- country : str
- city : str
- state : str
- store manager : str
- number of employees : int
- created at : datetime

-- Employees Table --
- id : serial num (6 digit)
- restaurant id : fk Restaurant
- name : str
- clocked in : boolean
- hours : numeric
- created at : datetime

-- Positions Table --
- id : serial num
- name : str

-- Employee_Position --
- id : serial num
- employee_id : fk Employee
- position_id : fk Position

-- Menu Table --
- id : serial num (6 digits)
- name : str 
- price : numeric
- description : str 
- created at : datetime

-- Ingredient Table --
- id : serial num (6 digit)
- name : str
- price : numeric
- created at : datetime

-- Ingredient Menu Table --
- id : serial num (6 digit)
- menu_id : fk Menu
- ingredient_id : fk Ingredient


-- Inventory Table --
- id : serial num (6 digits)
- ingredient_id : fk Ingredients
- quantity : int
- created at : datetime

-- Discounts Table --
- id : serial num (4 digit)
- name : str
- percent : numeric
- created at : datetime

-- Orders Table --
- id : serial num (12 digits)
- employee : fk Employee
- number of guests : int (can aggregate later)
- num items : int (can aggreate later)
- bill total : numeric (stored and updated in real time)
- paid : boolean
- created at : datetime

-- Order Items Table -- 
- id : serial num (6 digit)
- order_id : fk Order
- menu_id : fk Menu
- discount : fk Discount
- seat_num : int
- quantity : int 
- instructions : str

-- Payment Table --
- id : serial num
- order_id : fk Order
- provider : str
- provider_payment_id : int
- amount : numeric
- method : str
- status : str
- created_at : datetime

-- Tips Table -- 
- id : serial num (6 digit)
- order : fk Order 
- employee : fk Employee
- payment : fk Payment
- total : bill total Orders Table
- tip amount : numeric 

-- Tables Table --
- id : serial num (6 digit)
- table number : int
- is assigned : boolean
- employee : fk Employee default Null
- order : fk Orders default Null
- status : str
- party : list table numbers default Null
- created at : datetime

-- Reservations Table --
- id : serial num (6 digits)
- datetime : datetime
- name : str
- number of guests : int
- email : str
- phone number : str


