<h1 class="code-line">Project 5: Circular Double-Ended Queues (Deque)</h1>
<p class="code-line"><strong>Due: Thursday, March 3rd @ 10:00pm pm EST</strong></p>
<p class="code-line"><em>This is not a team project, do not copy someone else&rsquo;s work.</em></p>
<p class="code-line"><em><img src="https://s3.amazonaws.com/mimirplatform.production/files/ee009eaf-1d8b-4a24-8e62-722a6db1ef29/CircularDeque.png" alt="CircularDeque.png" /></em></p>
<h2 class="code-line">Assignment Overview</h2>
<p>In a typical FIFO (First in First out) queue, elements are added to one end of the underlying structure and removed from the opposite. These are natural for storing sequences of instructions: Imagine that instructions are added to the queue when first processed, and removed when completed. The first instruction processed will also be the first completed - we add it to the front, and remove it from the back.</p>
<p>A deque is a <a href="https://en.wikipedia.org/wiki/Double-ended_queue">double-ended queue</a>, meaning elements can be added or removed from either end of the queue. This generalizes the behavior described above to account for more complex usage scenarios. The ability to add or remove from both ends of the deque allows the structure to be used as both a FIFO queue and a LIFO stack, simultaneously.</p>
<p>This structure is useful for storing undo operations, where more recent undos are pushed and popped from the top of the deque and old/expired undo are removed from the back of the deque. Trains, consisting of sequences of cars, can also be thought of as deques: cars can be added or removed from either end, but never the middle.</p>
<p>A circular queue is a queue of fixed size with end-to-end connections. This is a way to save memory as deleted elements in the queue can simply be overwritten. In the picture above at index 0, element 1 has been removed (dequeued) from the queue but the value remains. If two new values are enqueued, then that 1 will be overwritten. After this, the circular queue will have reached capacity, and need to grow.</p>
<p>Circular queues are useful in situations with limited memory. Consider a router in an internet network. A package (a set of bits sent across the network) is sent to this router and it joins the router's processing queue. This router can only hold so many packets before it has to start dropping some. A circular queue would be useful here, as it optimizes memory usage.</p>
<p>A circular deque is a combination of a deque and a circular queue. It sets a max size and can grow and shrink like a circular queue, and it can enqueue/dequeue from both ends.</p>
<p>There are many equivalent implementations of circular deques, each with their own rationale and use cases. For this project you will implement a circular deque using both a circular array and a circular doubly linked list (CDLL) as underlying structures. A function,&nbsp;<strong>plot_speed</strong>, is provided for comparison of the two structures.</p>
<h2 class="code-line">Assignment Notes</h2>
<p>TIPS:</p>
<ul>
<li>The use of <a href="https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations">modulo (%)</a> is highly recommended</li>
<li>Understand what <a href="https://medium.com/@satorusasozaki/amortized-time-in-the-time-complexity-of-an-algorithm-6dd9a5d38045">amortized runtime</a> is (also explained below)</li>
<li>Enqueue and Dequeue both have basic tests which test their functionality in conditions where shrink and grow will not be called. This allows you to test your enqueue and dequeue functions without having to implement grow/shrink.</li>
<li>Although the API lists enqueue/dequeue first, it is common to implement grow/shrink and then enqueue/dequeue or grow-&gt;enqueue then shrink-&gt;dequeue. The test cases are designed to allow you to implement these functions independently in the order which best suits you.</li>
<li><b>Due to dependency issues with matplotlib on Mimir, we've rolled back the Mimir testcases to use Python 3.7 instead of Python 3.8.</b> This should not affect you unless you're using the walrus operator or some other obscure <a href="https://docs.python.org/3/whatsnew/3.8.html">new feature released in Python 3.8</a> which was not previously available in Python 3.7. We know that many of you are working with Python 3.8, 3.9, and 3.10 locally, and we make every effort to ensure cross-version compatibility of testcases—but at the end of the day, know that Mimir is running tests in Python 3.7.
</li>
</ul>
<p>RULES:</p>
<ul>
<li>The use of Python's Queues library is&nbsp;<strong>NOT ALLOWED</strong> and any use of it will result in a 0 on this project</li>
<li>The use of <span style="font-family: 'courier new', courier, monospace;">.pop()</span> is&nbsp;<strong>PROHIBITED. </strong>
<ul>
<li>Any function using .pop() will be deducted all points for test cases and manual grading</li>
<li><span style="font-family: 'courier new', courier, monospace;">.pop(x)</span> has a runtime of&nbsp;<em>O(n-x)</em>, where&nbsp;<em>n</em> is the length of the python list&nbsp;<span style="font-family: 'courier new', courier, monospace;">.pop(x)<span style="font-family: geomanist, sans-serif;"> is called on - in most situations, this will violate time complexity.&nbsp;</span></span></li>
</ul>
</li>
<li><span style="font-family: 'courier new', courier, monospace;"><span style="font-family: geomanist, sans-serif;">Use of the&nbsp;<strong>nonlocal&nbsp;</strong>keword will result in a 0 on the function is used on</span></span>
<ul>
<li><span style="font-family: 'courier new', courier, monospace;"><span style="font-family: geomanist, sans-serif;">You should never need to use this keyword in this project and if you are using it in a function in this class, you're doing something wrong.</span></span></li>
</ul>
</li>
</ul>
<h2 class="code-line">Assignment Specifications</h2>
<h4>class CircularDeque:</h4>
<p><em>DO NOT MODIFY the following attributes/functions</em></p>
<ul>
<li><strong>Attributes</strong>
<ul>
<li><strong>capacity: int:</strong> the total amount of items that can be placed in your circular deque. This grows and shrinks dynamically, but is never less than 4. Will always be greater than or equal to ;<strong>size</strong>.</li>
<li><strong>size: int:</strong> the number of items currently in your circular deque</li>
<li><strong>queue: list[T]:</strong> The underlying structure holding the data of your circular deque. Many elements may be&nbsp;<strong>None</strong>&nbsp;if your current&nbsp;<strong>size</strong> is less than&nbsp;<strong>capacity</strong>. This grows and shrinks dynamically.</li>
<li><strong>front: int:</strong> an index indicating the location of the first element in the circular deque</li>
<li><strong>back: int:</strong> an index indicating the location of the last element in your circular deque</li>
</ul>
</li>
<li><strong>__init__(self, data: list[T], front: int, capacity: int) -&gt; None</strong>
<ul>
<li>Constructs a circular deque</li>
<li><strong>data: list[T]:</strong> a list containing all data to be inserted into the circular deque</li>
<li><strong>front: int:&nbsp;</strong>An index to offset the front pointer to test the circular behavior of the list without growing</li>
<li><strong>capacity: int:&nbsp;</strong>the capacity of the circular deque</li>
<li><strong>Returns:&nbsp;</strong>None</li>
</ul>
</li>
<li><strong>__str__(self) -&gt; str</strong> and <strong>__repr__(self) -&gt; str</strong>
<ul>
<li>Represents the circular deque as a string</li>
<li><strong>Returns:&nbsp;</strong>str</li>
</ul>
</li>
</ul>
<p><em>IMPLEMENT the following functions</em></p>
<ul>
<li><strong>__len__(self) -&gt; int</strong>
<ul>
<li><span style="background-color: transparent;">Returns the length/size of the circular deque - this is the number of items currently in the circular deque, and will not necessarily be equal to the <strong>capacity</strong></span></li>
<li><span style="background-color: transparent;">This is a <a href="https://www.tutorialsteacher.com/python/magic-methods-in-python">magic method</a> and can be called with <strong>len(object_to_measure)</strong></span></li>
<li><span style="background-color: transparent;">Time complexity: <em>O(1)</em></span></li>
<li>Space complexity: <em>O(1)</em></li>
<li><strong>Returns:</strong> int representing length of the circular deque</li>
</ul>
</li>
<li><strong>is_empty(self) -&gt; bool</strong><br />
<ul>
<li>Returns a boolean indicating if the circular deque is empty</li>
<li>Time complexity: <em>O(1)</em></li>
<li>Space complexity: <em>O(1)</em></li>
<li><strong>Returns:</strong> True if empty, False otherwise</li>
</ul>
</li>
<li><strong>front_element(self) -&gt; T</strong><br />
<ul>
<li>Returns the first element in the circular deque</li>
<li>Time complexity: <em>O(1)</em></li>
<li>Space Complexity: <em>O(1)</em></li>
<li><strong>Returns:</strong> the first element if it exists, otherwise None</li>
</ul>
</li>
<li><strong>back_element(self) -&gt; T</strong><br />
<ul>
<li>Returns the last element in the circular deque</li>
<li>Time complexity: <em>O(1)</em></li>
<li>Space complexity: <em>O(1)</em></li>
<li><strong>Returns:</strong> the last element if it exists, otherwise None</li>
</ul>
</li>
<li><strong>enqueue(self, value: T, front: bool = True) -&gt; None:</strong><br />
<ul>
<li>Add a value to either the front or back of the circular deque based off the parameter <strong>front</strong></li>
<li>if front&nbsp;is true, add the value to the front. Otherwise, add it to the back</li>
<li>Call <strong>grow() </strong>if the size of the list has reached capacity</li>
<li><strong>param value: T:</strong> value to add into the circular deque</li>
<li><strong>param value front:&nbsp;</strong>where to add value T</li>
<li>Time complexity: <em>O(1)*</em></li>
<li>Space complexity: <em>O(1)*</em></li>
<li><strong>Returns:</strong> None</li>
</ul>
</li>
<li><strong>dequeue(self, front: bool = True) -&gt; T:</strong><br />
<ul>
<li>Remove an item from the queue</li>
<li>Removes the front item by default, remove the back item if False is passed in</li>
<li>Calls&nbsp;<strong>shrink() </strong>If the current size is less than or equal to 1/4 the current capacity, and 1/2 the current capacity is greater than or equal to 4, halves the capacity.</li>
<li><strong>param front:</strong> Whether to remove the front or back item from the dequeue</li>
<li>Hint: You shouldn't delete the value from the dequeue (by setting it to None) as that spot will merely be overwritten when you enqueue on that spot so it's more efficient to only adjust the back/front pointer instead.</li>
<li>Time complexity: <em>O(1)*</em></li>
<li>Space complexity: <em>O(1)*</em></li>
<li><strong>Returns: </strong>removed item,&nbsp;None if empty</li>
</ul>
</li>
<li><strong>grow(self) -&gt; None</strong>
<ul>
<li>Doubles the capacity of CD by creating a new underlying python list with double the capacity of the old one and copies the values over from the current list.</li>
<li>The new copied list will be 'unrolled' s.t. the front element will be at index 0 and the tail element will be at index [size - 1].&nbsp;</li>
<li>Time complexity: <em>O(n)</em></li>
<li>Space complexity: <em>O(n)</em></li>
<li><strong>Returns:&nbsp;</strong>None</li>
</ul>
</li>
<li><strong>shrink(self) -&gt; None</strong>
<ul>
<li>Cuts the capacity of the queue in half using the same idea as grow. Copy over contents of the old list to a new list with half the capacity.</li>
<li>The new copied list will be 'unrolled' s.t. the front element will be at index 0 and the tail element will be at index [size - 1].&nbsp;</li>
<li>Will never have a capacity lower than 4,&nbsp;<strong>DO NOT&nbsp;</strong>shrink when shrinking would result in a capacity &lt;= 4</li>
<li>Time complexity: <em>O(n)</em></li>
<li>Space complexity: <em>O(n)</em></li>
<li><strong>Returns:&nbsp;</strong>None</li>
</ul>
</li>
</ul>
<p>*<strong><a href="https://medium.com/@satorusasozaki/amortized-time-in-the-time-complexity-of-an-algorithm-6dd9a5d38045">Amortized</a></strong>. <em>Amortized Time Complexity</em> means 'the time complexity a majority of the time'. Suppose a function has amortized time complexity&nbsp;<em>O(f(n))</em> - this implies that the majority of the time the function falls into the complexity class <em>O(f(n)), </em>however, there may exist situations where the complexity exceeds <em>O(f(n)). </em>The same logic defines the concept of&nbsp;<em>Amortized Space Complexity</em>.</p>
<div><span style="text-decoration: underline;">Example</span>:&nbsp; <span style="font-family: 'courier new', courier, monospace;">enqueue(self, value: T, front: bool)<span style="font-family: geomanist, sans-serif;">has an amortized time complexity of&nbsp;<em>O(1)</em>:&nbsp;In the majority of situations, enqueueing an element occurs through a constant number of operations. However, when the Circular Deque is at capacity,&nbsp;grow(self) is called - this is an <em>O(n)&nbsp;</em>operation, therefore in this particular scenario, enqueue exceeds its amortized bound.</span></span></div>
<h3 class="code-line"><span style="font-size: 1.5em; background-color: transparent;">The (not) Application </span><span style="font-size: 1.5em; background-color: transparent;">Overview:</span><span style="font-size: 1.5em; background-color: transparent;"><em> Another Circular Deque!!!</em></span><span style="font-size: 1.5em; font-weight: bold; background-color: transparent;"><em><br /></em></span></h3>
<p class="code-line"><img src="https://s3.amazonaws.com/mimirplatform.production/files/65515d69-b790-491e-8a44-391f87d56794/boss-yells-at-employee.jpg" alt="boss-yells-at-employee.jpg" /></p>
<p class="code-line">After graduation, you've been hired by an exciting new tech start-up based out of silicon valley. On the first day, your new supervisor, Charles C. "not the MSU Professor" Owen has a quote for you: "there is a word for people who implement circular deques utilizing python lists as the underlying structure: unemployed."</p>
<p class="code-line">As you mull about the office on your first day, you hear horror stories. This guy hates lists! He flies into an explicable rage whenever he sees one. The threat is clear: if you use a python list for your first assignment, creating a circular deque class for the companies internal use, you'll be fired.</p>
<p class="code-line">Luckily, Charles "If you use a list, you will face my fists" Owen has provided for your use his own class: the&nbsp;<strong>CDLL (Circular Doubly Linked List)</strong>. It isn't perfect, but it will get the job done.</p>
<p class="code-line">Throughout the body of this project, you have created an interface via the methods of the&nbsp;<strong>CircularDeque</strong> class for a more complex structure below. Functions such as&nbsp;<strong>grow</strong> and&nbsp;<strong>shrink</strong> would never be called by a user of the class during a typical use case, and the underlying data array never accessed directly - in many languages, such as C++, access to these functions and variables may be restricted entirely to create a simplified forward facing API.</p>
<h3 class="code-line"><strong>Expectations</strong>:</h3>
<p><img src="https://s3.amazonaws.com/mimirplatform.production/files/13f4a0ec-1dd0-402e-93f3-1eeda07ea2f0/circular-doubly-linked-list.png" alt="circular-doubly-linked-list.png" /></p>
<p class="code-line">You are given the classes described below.&nbsp;<strong>DO NOT</strong> modify these classes - any modification will result in a zero for this portion of the project.</p>
<p class="code-line"><strong>class CDLLNode</strong></p>
<p class="code-line"><em>DO NOT MODIFY the following attributes/functions</em></p>
<ul>
<li class="code-line"><strong>Attributes:</strong>
<ul>
<li class="code-line"><strong>val: T: </strong>value stored by the node</li>
<li class="code-line"><strong>next: CDLLNode:&nbsp;</strong>The next node in the&nbsp;<strong>CDLL</strong></li>
<li class="code-line"><strong>prev: CDLLNode:</strong> The previous node in the&nbsp;<strong>CDLL</strong></li>
</ul>
</li>
<li><strong>__init__(self, val: T, next: CDLLNode = None, prev: CDLLNode = None) -&gt; None</strong>
<ul>
<li>Constructs a <strong>CDLLNode</strong></li>
<li><strong>param val:&nbsp;</strong>value stored by the node</li>
<li><strong>param next: CDLLNode:&nbsp;</strong>The next node in the&nbsp;<strong>CDLL</strong></li>
<li><strong>param prev: CDLLNode:&nbsp;</strong>The next node in the&nbsp;<strong>CDLL</strong></li>
<li><strong>return: None</strong></li>
</ul>
</li>
<li><strong>__eq__(self, other: CDLLNode) -&gt; bool</strong>
<ul>
<li>Compares two <strong>CDLLNode&nbsp;</strong>objects by value</li>
<li><strong>param other: CDLLNode:&nbsp;</strong>The other node</li>
<li><strong>return:&nbsp;</strong>True if the comparison is true, else false</li>
</ul>
</li>
<li><strong>__str__(self) -&gt; str</strong>
<ul>
<li>returns a string representation of the <strong>CDLLNode</strong></li>
<li><strong>return:&nbsp;</strong>a string</li>
</ul>
</li>
</ul>
<p><strong>class CDLL:</strong></p>
<p><em>DO NOT MODIFY the following attributes/functions</em></p>
<ul>
<li><strong>Attributes:</strong>
<ul>
<li><strong>head: CDLLNode:&nbsp;</strong>The head of the&nbsp;<strong>CDLL</strong></li>
<li><strong>size: int:&nbsp;</strong> the number of nodes in the&nbsp;<strong>CDLL</strong></li>
</ul>
</li>
<li><strong>__init__(self) -&gt; None</strong><br />
<ul>
<li>Creates a&nbsp;<strong>CDLL</strong></li>
<li><strong>return: None</strong></li>
</ul>
</li>
<li><strong>__eq__(self, other: CDLL) -&gt; bool:</strong>
<ul>
<li>Compares two <strong>CDLL&nbsp;</strong>objects by value</li>
<li><strong>param other: CDLL:&nbsp;</strong>the other list to compare</li>
<li><strong>return:&nbsp;</strong>True if the comparison is true, else false</li>
</ul>
</li>
<li><strong>__str__(self) -&gt; str</strong><br />
<ul>
<li>returns a string representation of the&nbsp;<strong>CDLL</strong></li>
<li><strong>return:&nbsp;</strong>a string</li>
</ul>
</li>
<li><strong>insert(self, val: T, front: bool = True) -&gt; None:</strong>
<ul>
<li>inserts a node with value <strong>val</strong> in the front or back of the&nbsp;<strong>CDLL</strong></li>
<li><strong>param val: T:&nbsp;</strong>the value to insert</li>
<li><strong>param front: bool = True:&nbsp;</strong> whether to insert in the front of the list, or the back.</li>
<li><strong>return: None</strong></li>
</ul>
</li>
<li><strong>remove(self, front: bool = True) -&gt; None:</strong>
<ul>
<li>removes a node from the <strong>CDLL</strong></li>
<li><strong>param front: bool = True:&nbsp;</strong>whether to remove from the front of the list, or the back</li>
<li><strong>return: None</strong></li>
</ul>
</li>
</ul>
<p>Your mission is to reimplement the functionality of&nbsp;<strong>CircularDeque</strong> with a&nbsp;<strong>CDLL&nbsp;</strong>as the underlying structure.</p>
<p><strong>class CDLLCD:</strong></p>
<p><strong>You are required to implement the following two functions:</strong></p>
<ul>
<li><strong>enqueue(self, val: T, front: bool = True) -&gt; None</strong>
<ul>
<li>adds a value to the <strong>CDLLCD</strong></li>
<li><strong>param val: T:&nbsp;</strong>the value to be added</li>
<li><strong>param front: bool = True:&nbsp;</strong>whether to add to the front or the back of the deque</li>
<li>Time complexity: <em>O(1)</em></li>
<li>Space complexity: <em>O(1)</em></li>
<li><strong>return: None</strong></li>
</ul>
</li>
<li><strong>dequeue(self, front: bool = True) -&gt; T</strong>
<ul>
<li>Removes a value from the deque, returning it</li>
<li><strong>param front: bool = True:&nbsp;</strong>whether to remove from the front or the back of the deque</li>
<li>Time complexity: <em>O(1)</em></li>
<li>Space complexity: <em>O(1)</em></li>
<li><strong>return: The dequeued element, none if empty</strong></li>
</ul>
</li>
</ul>
<p><strong>Three other functions are provided. YOU MAY MODIFY THESE IN ANY WAY YOU PLEASE, INCLUDING TO ADD ATTRIBUTES TO THE CLASS:</strong></p>
<ul>
<li><strong>__init__(self) -&gt; None</strong>
<ul>
<li>Creates a <strong>CDLLCD&nbsp;</strong>object</li>
<li><strong>return: None</strong></li>
</ul>
</li>
<li><strong>__eq__(self, other: CDLLCD) -&gt; bool</strong>
<ul>
<li>compares two&nbsp;<strong>CDLLCD</strong> objects by value</li>
<li><strong>param other:&nbsp;</strong> the other&nbsp;<strong>CDLLCD</strong></li>
<li><strong>return:&nbsp;</strong>True if the comparison evaluates to true, else false</li>
</ul>
</li>
<li class="code-line"><strong>__str__(self) -&gt; str:</strong><br />
<ul>
<li class="code-line">returns a string representation of the&nbsp;<strong>CDLLCD</strong></li>
<li class="code-line"><strong>return:&nbsp;</strong>a string</li>
</ul>
</li>
</ul>
<h2>Guarantees/Notes</h2>
<ul>
<li>You must actually use the underlying&nbsp;<strong>CDLL&nbsp;</strong>in the provided skeleton class. The testcase check for this, but attempting to get around the checks will result in a zero.</li>
<li>In his list-fuel rage, your boss yelled something about a <a href="https://en.wikipedia.org/wiki/Sentinel_node">sentintel node.</a> May be worth checking out...</li>
<li>Once completed, try running the function&nbsp;<strong>plot_speed</strong> to see how your implementation compares to the main project implementation. They should be pretty close.</li>
</ul>
<h2>Submission</h2>
<h4 class="code-line">Deliverables</h4>
<p class="code-line">Be sure to upload the following deliverables in a .zip folder to Mimir by 11:59p Eastern Time on Friday, 03/03/22.</p>
<p class="code-line">Your .zip folder can contain other files (for example, specs.md and tests.py), but must include (at least) the following:</p>
<pre class="code-line"><code>|- Project5.zip
    |&mdash; Project5/
        |&mdash; feedback.xml          (for project feedback)
        |&mdash; __init__.py         (for proper Mimir testcase loading)       
        |&mdash; solution.py    (contains your solution source code)
</code></pre>
<h4 class="code-line"><strong>Grading</strong></h4>
<p class="code-line">The following 100-point rubric will be used to determine your grade on Project4:</p>
<ul>
<li class="code-line">Tests (70)<br />
<ul>
<li>00 - Coding Standard: __/3</li>
<li class="code-line">01 - len(): __/2</li>
<li class="code-line">02 - is_empty: __/2</li>
<li class="code-line">03 - front_element: __/2</li>
<li class="code-line">04 - back_element: __/2</li>
<li class="code-line">05 - front_enqueue_basic: __/2</li>
<li>06 - back_enqueue_basic: __/2</li>
<li class="code-line">07 - front_enqueue: __/5</li>
<li class="code-line">08 - back_enqueue: __/5</li>
<li class="code-line">09 - front_dequeue_basic: __/2</li>
<li>10 - back_dequeue_basic: __/2</li>
<li class="code-line">11 - front_dequeue: __/5</li>
<li class="code-line">12 - back_dequeue: __/5</li>
<li class="code-line">13 - grow: __/4</li>
<li class="code-line">14 - shrink: __/4</li>
<li class="code-line">15 - Circular Deque Comprehensive: __/10</li>
<li class="code-line">16 - Application: __/10</li>
<li>99 - Feedback.xml: __/3</li>
</ul>
</li>
<li class="code-line">Manual (30)
<ul>
<li class="code-line">M0 - len(): __/1</li>
<li>M1 - is_empty: __/1</li>
<li>M2 - front_element: __/2</li>
<li>M3 - back_element: __/2</li>
<li>M4 - front_enqueue: __/3</li>
<li>M5 - back_enqueue: __/3</li>
<li>M6 - front_dequeue: __/3</li>
<li>M7 - back_dequeue: __/3</li>
<li>M8 - grow: __/3</li>
<li>M9 - shrink: __/3</li>
<li>M10 - application: __/6</li>
</ul>
</li>
</ul>
<p class="code-line"><em>This project was created by Jacob Caurdy and Andrew Haas</em></p>
<p class="code-line"><em>Inspired by previous 331&nbsp; CircularDeque project created by Angelo Savich and Olivia Mikola</em></p>
