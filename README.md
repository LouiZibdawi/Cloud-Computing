## Set up AWS environment

Add credentials to:
`~/.aws/credentials`

Add region to:
`~/.aws/config`

---

## Set up Azure environment

Find the connection in: **Storage Account -> Access Keys -> Connection string**

Run the following with the connection string to set the connection environment variable:

```
export AZURE_STORAGE_CONNECTION_STRING=[INSERT_CONNECTION_STRING]
```

---

## Task 1 - Creating Buckets/Containers and Objects/Blobs

Create buckets and objects in AWS:

```
cd aws
```

**or** to for create containers and blobs in Azure:

```
cd azure
```

Create:

```
python task1_createContent
```

Interface:

```
python task1_showMenu
```

Follow the instructions on the screen, entering integers where neccessary as well as strings

```
=================================
Select one the following options:
=================================
1. Display objects in all containers
2. Display objects in specific container
3. Display object with a specific name
4. Download object by name
5. Exit
=================================
```

---

## Task 2 - Building and querying a database in AWS

Build the database

```
python task2_buildDB
```

Query the database

```
python task2_queryDB
```

Input guide for query

```
# Primary key is year
Primary/Partition Key [(1) Individual (2) Range (3) None]: (Valid inputs: 1, 2 or 3)

# Secondary key is title
Secondary/Sort Key [(1) Individual (2) Range (3) None]: (Valid inputs: 1, 2 or 3)

# Select the name of filter if you want one
Filter name [(1) rank, (2) rating, (3) runtime (4) None]: (Valid inputs: 1, 2, 3 or 4)

# If selected a filter name, select the filter expression
Filter expression [(1) equal to (2) less than (3) greater than]: (Valid inputs: 1, 2 or 3)

# If selected a filter name, select a filter value
Filter value (double): (Valid inputs: double)

# Sort by either year (primary), title (secondary) or other which can be any column you enter.
Sort [(1) Primary (2) Secondary (3) Other (4) None]:

# List of comma separated column names
Fields/Attributes [Separate by comma, leave blank for none]:

# Print to csv or terminal
Save to CSV? [(0) no, (1) yes]:
```

Notes for implementation:

- Sort is always descending
- Default fields if left blank are year and title
- If save to CSV, it will not print on terminal
- If not saved to CSV it will print to the terminal

---

## Task 2 - Building and querying a database in Azure

Will be handed in on Friday, January 31st, 2020
