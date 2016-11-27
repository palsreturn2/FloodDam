# FloodDam (A Distributed Flood Data Acquisition and Management Framework)

# Synopsis

This is a framework that is built for acquiring data during Natural Disasters (Flood as a case study) and using the data for preparing relief for the affected people. The framework consists of a distributed replicated database where disaster data will be stored during disasters. The problem of maintaining consistency in the replicated database is done using a token based algorithm based on a floating Single Master (Master floats with the token). The algorithm is very similiar to Raymond's token based algorithm in Distributed Computing for Mutual Exclusion. The only difference is that in Raymond's algorithm the directed tree formed can have height greater than 2 but in this case height is 2 only (One Master and all other clients connected to it). The Clients have no connection in between them.

# Motivation

In case of natural calamities, certain zones become hotspots. Data acquisition becomes important during that time so that relief can be arranged. There are various applications and frameworks for data acquisition but they all assume central database. This assumption works when the coverage area is less but becomes extremely slow when area increases. Hence this framework uses a distributed database for data acquisition. The rest of the framework basically deals with the problems of mutual exclusion and data reads and writes.
