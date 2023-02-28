Project 9: Graphs Part 1
========================

**Due: Thursday, April 14 @ 10:00 pm**

_This is not a team project, do not copy someone else’s work._

_Project based on contributions by Adam Kasumovic, Andrew Haas, Brooke Osterkamp, Andrew McDonald, Tanawan Premsri, and Andy Wilson._

Assignment Overview
-------------------

Graphs are particularly useful data structures for modeling connections and relationships among objects. In fact, you've likely used an application that relies on graphical modeling today - a few examples include:

* **Facebook / Twitter / Instagram**
    * Users are modeled as vertices storing posts, photos, videos, etc.
    * Edges are modeled as "friendships," "followers," "likes," "favorites," etc.
* **Google / Apple / Bing Maps**
    * Intersections, cities, and other points of interest are modeled by vertices
    * Road segments between intersections are modeled by weighted edges, where weights represent the relative
      speed/traffic of the road segment

You will be implementing a **directed, weighted** Graph ADT using the **adjacency map** design, in which a graph object consists of a map (ordered dictionary) of vertices, and each vertex holds its own map (ordered dictionary) of adjacent vertices, i.e. vertices to which that vertex is connected by an outgoing edge.

For more depth information on Graphs make sure to check
[D2L-Week-10-11-12](https://d2l.msu.edu/d2l/le/content/1676253/Home), lecture slides and Graph ADT source code is all
uploaded on D2L.

In some ways, this project (along with Project 10) also serves as a capstone to the course; in completing it one utilizes recursion, queues, two-dimensional arrays, hash maps, dynamic programming, and more. You may also notice that trees, linked lists, and even heaps are special cases of the general graph structure and that many graph algorithms can be applied to these earlier structures without modification. To highlight this inheritance, consider the inorder traversal algorithm we applied to AVL trees; really, it was nothing more than a graph depth-first search with a tendency to go left before right.

The goal of this project (along with Project 10) is to introduce the versatile and flexible nature of graphs, along with the operations and search algorithms that make them so useful.

![got_graph.png](https://s3.amazonaws.com/mimirplatform.production/files/aea24196-db6a-46f0-9008-3ff19b7d29c7/got_graph.png)

Assignment Notes
----------------

* A plotting function is provided to help you visualize the progression of various search algorithms
    * Be sure to read the specs explaining **plot()**
    * If you don't want to use it, just comment out the related import statements and **plot()** function
* Python allows representation of the value infinity using **float('inf')**
* No negative edge weights will ever be added to the graph
    * All edge weights are numeric values greater than or equal to zero
* Time complexities are specified in terms of *V* and *E*, where *V* represents the number of vertices in the
  graph and *E* represents the number of edges in a graph
    * Recall that *E* is bounded above by *V*^2; a graph has *E* = *V*^2 edges if and only if every vertex is
      connected to every other vertex
* Recall that **list.insert(0, element)** and **list.pop(0)** are both _O(N)_ calls on a Python list
    * Recall that python's 'lists' are not lists in the more common sense of the word: linked lists. They are
      dynamically managed tuples, stored in memory as contiguous arrays of pointers to elements elsewhere in memory.
      This allows indexing into a 'list' in constant time. The downside of this, however, is that adding to a python '
      list' at a specific index, _i,_ requires shifting the pointer to every element past _i_ by one in the underlying
      array: a linear operation.
    * Be careful when implementing **bfs and dfs** to ensure you do not break time complexity by popping or inserting
      from the front of a list when reconstructing a path
    * Instead of inserting into / popping from the front of the list, simply append to or pop from the end, then reverse
      the list _once_ at the end
        * If you have N calls to **list.insert(0, element)**, that is _O(N^2)_
        * If you instead have N calls to **list.append(element)**, followed by a single call to **list.reverse()**, that
          is _O(N)_
        * Both methods will result in the same list being constructed, but the second is far more efficient

Assignment Specifications
-------------------------

### class Vertex

Represents a vertex object, the building block of a graph.

**_DO NOT MODIFY the following attributes/functions_**

* **Attributes**
    * **id:** A string used to uniquely identify a vertex
    * **adj:** A dictionary of type **{other\_id : number}** which represents the connections of a vertex to other
      vertices; the existence of an entry with key **other\_i****d** indicates connection from this vertex to the vertex
      with id **other\_id** by an edge with weight **number**
        * Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries
          is guaranteed and ensures traversals will select the next neighbor to visit deterministically
    * **visited:** A boolean flag used in search algorithms to indicate that the vertex has been visited
    * **x:** The x-position of a vertex (defaults to zero)
    * **y:** The y-position of a vertex (defaults to zero)
* **\_\_init\_\_(self, idx: str, x: float=0, y: float=0) -> None:**
    * Constructs a Vertex object
* **\_\_eq\_\_(self, other: Vertex) -> bool:**
    * Compares this vertex for equality with another vertex
* **\_\_repr\_\_(self) -> str:**
    * Represents the vertex as a string for debugging
* **\_\_str\_\_(self) -> str:**
    * Represents the vertex as a string for debugging
* **\_\_hash\_\_(self) -> int:**
    * Allows the vertex to be hashed into a set; used in unit tests

**_IMPLEMENT the following functions_**

* **deg(self) -> int:**
    * Returns the number of outgoing edges from this vertex; i.e., the outgoing degree of this vertex
    * _Time Complexity: O(1)_
    * _Space Complexity: O(1)_
* **get\_outgoing\_edges(self) -> Set\[Tuple\[str, float\]\]:**
    * Returns a **set** of tuples representing outgoing edges from this vertex
    * Edges are represented as tuples **(other\_id, weight)** where
        * **other\_id** is the unique string id of the destination vertex
        * **weight** is the weight of the edge connecting this vertex to the other vertex
    * Returns an empty set if this vertex has no outgoing edges
    * _Time Complexity: O(degV)_
    * _Space Complexity: O(degV)_
* **euclidean\_dist(self, other: Vertex) -> float:**
    * Returns the [euclidean distance](http://rosalind.info/glossary/euclidean-distance/) \[based on two-dimensional
      coordinates\] between this vertex and vertex **other**
    * Used in Project 10
    * _Time Complexity: O(1)_
    * _Space Complexity: O(1)_
* **taxicab\_dist(self, other: Vertex) -> float:**
    * Returns the [taxicab distance](https://en.wikipedia.org/wiki/Taxicab_geometry) \[based on two-dimensional
      coordinates\] between this vertex and vertex **other**
    * Used in Project 10
    * _Time Complexity: O(1)_
    * _Space Complexity: O(1)_

### class Graph

Represents a graph object

**_DO NOT MODIFY the following attributes/functions_**

* **Attributes**
    * **size:** The number of vertices in the graph
    * **vertices:** A dictionary of type **{id : Vertex}** storing the vertices of the graph, where **id** represents
      the unique string id of a **Vertex** object
        * Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries
          is guaranteed and ensures **get\_edges(self)** and **get\_vertices(self)** will return deterministically
          ordered lists
    * **plot\_show**: If true, calls to **plot()** display a rendering of the graph in matplotlib; if false, all calls
      to **plot()** are ignored (see **plot()** below)
    * **plot\_delay**: Length of delay in **plot()**  (see **plot()** below)
* **\_\_init\_\_(self, plt\_show: bool=False) -> None:**
    * Constructs a Graph object
    * Sets **self.plot\_show** to False by default
* **\_\_eq\_\_(self, other: Graph) -> bool:**
    * Compares this graph for equality with another graph
* **\_\_repr\_\_(self) -> str:**
    * Represents the graph as a string for debugging
* **\_\_str\_\_(self) -> str:**
    * Represents the graph as a string for debugging
* **add\_to\_graph(self, start\_id: str, dest\_id: str=None, weight: float=0) -> float:**
    * Adds a vertex / vertices / edge to the graph
        * Adds a vertex with id **start\_id** to the graph if no such vertex exists
        * Adds a vertex with id **dest\_id** to the graph if no such vertex exists and **dest\_id** is not None
        * Adds an edge with weight **weight** if **dest\_id** is not None
    * If a vertex with id **start\_id** or **dest\_id** already exists in the graph, this function will not overwrite
      that vertex with a new one
    * If an edge already exists from vertex with id **start\_id** to vertex with id **dest\_id**, this function will
      overwrite the weight of that edge
* **matrix2graph(self, matrix: Matrix) -> None:**
    * Constructs a graph from a given adjacency matrix representation
    * **matrix** is guaranteed to be a square 2D list (i.e. list of lists where # rows = # columns), of size **\[V+1\]**
      x **\[V+1\]**
        * **matrix\[0\]\[0\]** is None
        * The first row and first column of **matrix** hold string ids of vertices to be added to the graph and are
          symmetric, i.e. **matrix\[i\]\[0\] = matrix\[0\]\[i\]** for i = 1, ..., n
        * **matrix\[i\]\[j\]** is None if no edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]**
        * **matrix\[i\]\[j\]** is a **number** if an edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]** with weight **number**
* **graph2matrix(self) -> None:**
    * Constructs and returns an adjacency matrix from a graph
    * The output matches the format of matrices described in **matrix2graph**
    * If the graph is empty, returns **None**
* **graph2csv(self, filepath: str) -> None:**
    * Encodes the graph (if non-empty) in a csv file at the given location

**_USE the following function however you'd like_**

* **plot(self) -> None:**
    * Renders a visual representation of the graph using matplotlib and displays graphic in PyCharm
        * [Follow this tutorial to install matplotlib and numpy if you do not have them](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html)
          , or follow the tooltip auto-suggested by PyCharm
    * Provided for use in debugging
    * If you call this in your searches and **self.****plot\_show** is true, the search process will be animated in
      successive plot renderings (with time between frames controlled by **self.plot\_delay**)
    * Not tested in any testcases
        * All testcase graphs are constructed with **self.plot\_show** set to False
    * If vertices have (x,y) coordinates specified, they will be plotted at those locations
    * If vertices do not have (x,y) coordinates specified, they will be plotted at a random point on the unit circle
    * To install the necessary packages (matplotlib and numpy), follow the auto-suggestions provided by PyCharm
    * Vertices and edges are labeled; edges are color-coded by weight
        * If a bi-directional edge exists between vertices, two color-coded weights will be displayed

![sample_plot.png](https://s3.amazonaws.com/mimirplatform.production/files/0aec2496-150a-4b85-b86f-142f235fe4ba/sample_plot.png)

**_IMPLEMENT the following functions_**

* **unvisit\_vertices(self) -> None:**
    * Resets visited flags to False of all vertices within the graph
    * Used in unit tests to reset graph between tests
    * _Time Complexity: O(V)_
    * _Space Complexity: O(V)_
* **get\_vertex\_by\_id(self, v\_id: str) -> Vertex:**
    * Returns the Vertex object with id **v\_id** if it exists in the graph
    * Returns None if no vertex with unique id **v\_id** exists
    * _Time Complexity: O(1)_
    * _Space Complexity: O(1)_
* **get\_all\_vertices(self) -> Set\[Vertex\]:**
    * Returns a **set** of all **Vertex objects** held in the graph
    * Returns an empty set if no vertices are held in the graph
    * _Time Complexity: O(V)_
    * _Space Complexity: O(V)_
* **get\_edge\_by\_ids(self, begin\_id: str, end\_id: str) -> Tuple\[str, str, float\]:**
    * Returns the edge connecting the vertex with id **begin\_id** to the vertex with id **end\_id** in a tuple of the
      form **(begin\_id, end\_id, weight)**
    * If the edge or either of the associated vertices does not exist in the graph, returns **None**
    * _Time Complexity: O(1)_
    * _Space Complexity: O(1)_
* **get\_all\_edges(self) -> Set\[Tuple\[str, str, float\]\]:**
    * Returns a **set** of tuples representing all edges within the graph
    * Edges are represented as tuples **(begin\_id, end\_id, weight)** where
        * **begin\_id** is the unique string id of the starting vertex
        * **end\_id** is the unique string id of the destination vertex
        * **weight** is the weight of the edge connecting the starting vertex to the destination vertex
    * Returns an empty set if the graph is empty
    * _Time Complexity: O(V+E)_
    * _Space Complexity: O(E)_
* **build\_path(self, back\_edges: Dict\[str, str\], begin\_id: str, end\_id: str) -> Tuple\[List\[str\], float\]:**
    * Given a dictionary of back-edges (a mapping of vertex id to predecessor vertex id), reconstructs the path from start\_id to end\_id and computes the total distance
    * Helper function to **bfs** and **MUST BE CALLED THERE!**
    * Used in Project 10
    * Returns tuple of the form **(\[path\], distance)** where
        * **\[path\]** is a list of vertex id strings beginning with **begin\_id**, terminating with **end\_id**, and
          including the ids of all intermediate vertices connecting the two
        * **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * Handle the cases where no path exists from vertex with id **begin\_id** to vertex with **end\_id** or if one of the vertices does not exist in **bfs** (see below for more info).
    * _Time Complexity: O(V)_
    * _Space Complexity: O(V)_
* **bfs(self, begin\_id: str, end\_id: str) -> Tuple\[List\[str\], float\]:**
    * Perform a breadth-first search beginning at vertex with id **begin\_id** and terminating at vertex with id **end\_id**
    * **MUST CALL build\_path!**
    * **As you explore from each vertex, iterate over neighbors using vertex.adj (not vertex.get\_edges()) to ensure neighbors are visited in proper order**
    * Returns tuple of the form **(\[path\], distance)** where
        * **\[path\]** is a list of vertex id strings beginning with **begin\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        * **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * If no path exists from vertex with id **begin\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    * Guaranteed that **begin\_id != end\_id** (since that would be a trivial path)
    * Because our adjacency maps use [insertion ordering](https://stackoverflow.com/a/57072435), neighbors will be visited in a deterministic order, and thus you do not need to worry about the order in which you visit neighbor vertices at the same depth
    * Use the [SimpleQueue](https://docs.python.org/3/library/queue.html) class to guarantee O(1) pushes and pops on the queue
    * _Time Complexity: O(V+E)_
    * _Space Complexity: O(V)_
* **dfs(self, begin\_id: str, end\_id: str) -> Tuple\[List\[str\], float\]:**
    * Wrapper function for **dfs\_inner**, which MUST BE CALLED within this function
        * The majority of the work of dfs should be done in **dfs\_inner**
        * This function makes it simpler for client code to call for a dfs
        * This function makes it possible to avoid inserting vertex ids at the front of the path list on path reconstruction, which leads to sub-optimal performance (see Assignment Notes)
            * Hint: construct the path in reverse order in **dfs\_inner**, then reverse the path in this function to optimize time complexity
    * Hint: call **dfs\_inner** with **current\_id** as **begin\_id,** then reverse the path here and return it
    * _Time Complexity: O(V+E)  (including calls to dfs\_inner)_
    * _Space Complexity: O(V)  (including calls to dfs\_inner)_
* **dfs\_inner(self, current\_id: str, end\_id: str, path: List\[str\]=\[\]) -> Tuple\[List\[str\], float\]**
    * Performs the recursive work of depth-first search by searching for a path from vertex with id **current\_id** to vertex with id **end\_id**
    * **MUST BE RECURSIVE**
    * **As you explore from each vertex, iterate over neighbors using vertex.adj (not vertex.get\_edges()) to ensure neighbors are visited in proper order**
    * Returns tuple of the form **(\[path\], distance)** where
        * **\[path\]** is a list of vertex id strings beginning with **begin\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        * **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * If no path exists from vertex with id **current\_id** to vertex with **begin\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    * Guaranteed that **begin\_id != end\_id** (since that would be a trivial path)
    * Because our adjacency maps use [insertion ordering](https://stackoverflow.com/a/57072435), neighbors will be visited in a deterministic order, and thus you do not need to worry about the order in which you visit neighbor vertices
    * _Time Complexity: O(V+E)_
    * _Space Complexity: O(V)_
* **topological\_sort(self) -> List\[str\]:**
    * Performs topological sort on the graph, returning a possible topological ordering as a list of vertex ids.
    * Recall that there can be multiple correct orderings following topological sort, and the testcases will allow for any correct ordering.
    * Guaranteed that when this function is tested the graph is a connected DAG (Directed Acyclic Graph), although you may find it useful to ensure that this function properly "attempts" to sort cyclic connected directed graphs (i.e. this function does not crash when given a cyclic graph and just returns an invalid topological ordering).
    * You are provided with an **optional** empty **topological\_sort\_inner** function should you choose to use it in a recursive solution, although it is not required. You may remove it if you do not use it, and you may also modify its function signature.
    * Hint: There is a solution that is quite similar to your recursive implementation of **dfs** above which uses **topological\_sort\_inner** to traverse the graph in the same fashion as **dfs\_inner,** except this time you do not stop on an end\_id.
    * _Time Complexity: O(V+E) (including calls to topological\_sort\_inner)_
    * _Space Complexity: O(V) (including calls to topological\_sort\_inner)_

Application Problem
-------------------

![](https://image.api.playstation.com/vulcan/ap/rnd/202110/2000/aGhopp3MHppi7kooGE2Dtt8C.png)

**BRAVE TARNISHED, RISE, AND BECOME ELDEN LORD!**

_We salute you, worthy Tarnished for persevering through hardships to reach this point, but now you must embark on (Part 1) of your final journey._

[Elden Ring](https://en.wikipedia.org/wiki/Elden_Ring) is a game known for its high levels of difficulty, and like other games in its own [special genre](https://en.wikipedia.org/wiki/Soulslike), much of this difficulty comes from fighting challenging bosses. Unfortunately, this extreme difficulty is off-putting for a lot of players. As a new recruit to [FromSoftware](https://en.wikipedia.org/wiki/FromSoftware) 's team of game programmers, you've been tasked with rebalancing the game. [Miyazaki](https://en.wikipedia.org/wiki/Hidetaka_Miyazaki) has made it very clear that no changes to the actual bosses will be made. Instead, your teammates have proposed possible boss reorderings in the form of a connected, directed graph.

In such graphs, the vertices represent bosses, while the edges represent pairwise orderings in which the two bosses must be defeated. For example, an edge _**from**_ Margit _**to**_ Godrick i.e. ('Margit', 'Godrick') means that Margit must be defeated _**before**_ Godrick. In other words, Godrick will not be available until Margit has been defeated. Another way to think of it is that before visiting a vertex (defeating a boss), one must visit (defeat) _all_ vertices (bosses) with edges incoming to said vertex. Examples are provided below. We define the game with its boss ordering graph as _ beatable_ if and only if it is possible to defeat all bosses given by the graph while following the ordering rule denoted by the edges in the graph.

Your goal is to write a function for your Graph ADT that tells us if the boss ordering given by the graph produces a beatable game. Note that boss orderings may be partial (not include all bosses) and that there may be more than one order to defeat bosses in order to beat the game.

### Your Task

Implement the application solution function on your Graph ADT according to the following specifications

* **boss\_order\_validity(self) -> bool:**
    * Returns **True** if the game be beaten with the boss ordering represented by this graph, otherwise returns **False**
    * Be careful with time and space complexity, they are easy to violate here.
    * The testcases should give a good idea of when the game can be beaten or not.
    * Guaranteed that the graph is connected.
    * Consider an empty graph (no bosses) as already trivially beatable (return **True**).
    * Hint: You may find it useful to use your **topological\_sort** function to solve this problem, but it is not required.
    * _Time Complexity:_ _O(V+E)_
    * _Space Complexity: O(V)_

### Examples

Given the following graph (all plots made using the plot() function we provide you),

![myplot.png](https://i.imgur.com/IjpCY7F.png)

* **boss\_order\_validity()** would return **True**
    * Players can defeat Margit, then Godrick, and then Renalla.

Given the following graph,

![myplot.png](https://i.imgur.com/KNnfMB9.png)

* **boss\_order\_validity()** would return **False**
    * In order to defeat Renalla, Godrick must be defeated. In order to defeat Godrick, Margit must be defeated.
      However, in order to defeat Margit, Renalla must be defeated. It is impossible to beat the game!

Given the following graph,

![myplot.png](https://i.imgur.com/9wlOsvI.png)

* **boss\_order\_validity()** would return **True**
    * The bosses can be defeated in the following order: Godfrey, Morgott, Godskin Duo, Margit, Godrick, Renalla. Like
      the first case, there is only one order to defeat the bosses. (There may be multiple).

Submission
-----------

### Deliverables

Be sure to upload the following deliverables in a .zip folder to Mimir by 10:00 pm ET, on Thursday, April 14.

Project09.zip

        |— Project09/
                |— solution.py        (contains your solution code)
                |— feedback.xml       (for project feedback)
                |— __init__.py        (for proper Mimir testcase loading)

### Grading

* Tests (70)
    * Coding Standard: \_\_/3
    * feedback.xml Validity Check: \_\_/3
    * Vertex: \_\_/4
        * deg: \_\_/1
        * get\_outgoing\_edges: \_\_/1
        * distances: \_\_/2
    * Graph: \_\_/45
        * unvisit\_vertices: \_\_/1
        * get\_vertex\_by\_id: \_\_/2
        * get\_all\_vertices: \_\_/2
        * get\_edge\_by\_ids: \_\_/2
        * get\_all\_edges: \_\_/2
        * build\_path: \_\_/4
        * bfs: \_\_/8
        * dfs: \_\_/8
        * topological\_sort: \_\_/8
        * comprehensive: \_\_/8
    * Application: \_\_/15
        * boss\_order\_validity: \_\_/15
* Manual (30)
    * Loss of 1 point per missing docstring (max 3 point loss)
    * Loss of 2 points per changed function signature (max 20 point loss)
    * Time and space complexity points are **all-or-nothing** for each function. If you fail to meet time **or** space
      complexity in a given function, you do not receive manual points for that function.
    * Not using recursion when we tell you to (dfs\_inner) will result in a loss of half of all points associated with that function!
    * Not using build\_path will result in a loss of half of all points associated with bfs!
    * Time & Space Complexity (30)
        * M1 - deg, get\_outgoing\_edges, distances \_\_/3
        * M2 - unvisit\_vertices, get\_vertex\_by\_id, get\_all\_vertices, get\_edge\_by\_ids, get\_all\_edges \_\_/5
        * M3 - build\_path \_\_/2
        * M4 - bfs \_\_/3
        * M5 - dfs \_\_/5
        * M6 - topological\_sort \_\_/6
        * M7 - boss\_order\_validity \_\_/6
    * You must pass a given set of functions' automated tests to be eligible for manual points associated with that set
      of functions.
        * For example, to be eligible for complexity points on M2, you must pass all automated tests associated with
          get\_vertex\_by\_id, get\_all\_vertices, get\_edge\_by\_ids, get\_all\_edges
    * Any use of networkx or similar prewritten graph libraries in a function will result in a zero for all automated
      and manual points associated with that function.

Extra
------

![](https://i.imgur.com/J2M3jxq.png)

You can do it! *Ahem*, I mean,

_something incredible ahead_

_therefore don't give up!_

[Some music to listen to while working on this project :)](https://youtu.be/fi0NxuDUuv4)