# FloodDam (A Distributed Flood Data Acquisition and Management Framework)

# Synopsis

This is a framework that is built for acquiring data during Natural Disasters (Flood as a case study) and using the data for preparing relief for the affected people. The framework consists of a distributed replicated database where disaster data will be stored during disasters. The problem of maintaining consistency in the replicated database is done using a token based algorithm based on a floating Single Master (Master floats with the token). The algorithm is very similiar to Raymond's token based algorithm in Distributed Computing for Mutual Exclusion. The only difference is that in Raymond's algorithm the directed tree formed can have height greater than 2 but in this case height is 2 only (One Master and all other clients connected to it). The Clients have no connection in between them.

# Motivation

In case of natural calamities, certain zones become hotspots. Data acquisition becomes important during that time so that relief can be arranged. There are various applications and frameworks for data acquisition but they all assume central database. This assumption works when the coverage area is less but becomes extremely slow when area increases. Hence this framework uses a distributed database for data acquisition. The rest of the framework basically deals with the problems of mutual exclusion and data reads and writes.

# Installation and running

1) Download the codes in a folder in as many machines as you want to run the program.

2) Open the Master.py, Client.py and flaskr.py in each of the machines and change the variables "IP" and "MASTER_IP" with the machine's IP and master machine's IP. You can arbitrarily choose a Master machine.

3) Install flaskr. You need this to run the web service program.

4) Install sqlite3.

5) Create a database with schema given in "schema.sql" by executing the command "flask initdb".

6) Start the Master node you chose first by running the "Master.py" and "Client.py" program. Run the web service using "./run_flaskr.sh".

7) Then start the Client nodes also by running the "Master.py" and "Client.py" program. Start the web service using "./run_flaskr.sh".

8) Fire up the browser and go to the address "127.0.0.1:5000". This will open the web service in the current machine. To open the other web services from a single machine use the machine's IP instead of "127.0.0.1" .



