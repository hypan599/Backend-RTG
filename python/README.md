### Explanation
Here I use python3 to implement the management system.

### Dependency
Base python3 is needed, no other library is required.

In the code I've created classes for products, warehouse and "company" for holding all warehouses.
Class Company also provide interface for every command.

I use dictionary to store actual data since we are dealing with random access of data, and we are dealing with mapping of key values, not value itself.

### Usage
To start, run:
` python3 main.py `
and type in commands.


If getting commands from file, run:
` cat test_input.txt | python3 main.py `
please see test_input.txt for example of commands
