1.Download the database.
You can choose any database as long as it is in TXT format, with each line containing two numbers representing an edge between two nodes (an undirected edge in undirected graph algorithms, a directed edge in directed graph algorithms).
You can download databases from: (https://snap.stanford.edu/data/com-Orkut.html).

2.Preprocess the downloaded data.
Place the downloaded database into the "node hash" directory, then change `input_file.txt` in `node hash.py` to the name of the database you downloaded. After that, run `node hash.py`, and it will generate an `output_file.txt` file.

3.Choose the algorithm you want to run.
The "Undirected algorithms" directory contains all our undirected graph algorithms: Acc-Lap1Rd-U, Lap1Rd-U, Lap2Rd-U, Mod-Lap2Rd-U. Similarly, the "Directed algorithms" directory contains all our directed graph algorithms: Acc-Lap1Rd-D, Lap1Rd-D, Lap2Rd-D, Mod-Lap2Rd-D.

4.Run the algorithm.
Place the TXT file generated in step 2 into the directory of the algorithm you want to run ("Undirected algorithms" or "Directed algorithms"). Then, modify the `file_path` in the Python script of the algorithm you want to run to the name of the TXT file generated in step 2. Finally, run the corresponding algorithm to obtain the experimental results.


