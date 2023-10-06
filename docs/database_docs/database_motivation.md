Database management systems are specialized software to store and manage large scale data, and provides the ability to query data with optimized algorithms, and more.

2 main types of databases: relational and non-relational. 

**About relational databases and schemas**

Relational databases have a schema, which outlines the relations of the database. In other words, the schema is just the collection of tables, with all the attributes (columns) the database will have. Schemas offer guarantees, but it requires careful design to be effective. 

Schemas also require balancing tradeoffs depending on application. This includes the classic memory versus speed tradeoff. Another possible tradeoff might be between normalization and performance.

Database schemas development is an iterative process. Teams are encouraged to increase commitment to the working schema as it becomes more reliable.

**Why relational databases for us?**

We imagine that our product prioritizes accuracy - students and researchers need the right connections. The emphasis is on the matching of people to projects. I think relational databases will serve us well regarding our priority.

**How the database will be designed and implemented**

1. Discuss with potential users about the data they’d expect the system to have, to yield a natural description of the data needs. Collect some data for observation and database development
2. Draw an ER Diagram of the data based on the natural description.
3. Devise database schema from ER Diagram
4. Database implementation and testing:
   - Database definition
   - Data collection and insertion
   - Develop commonly used queries based on use cases collected by the project.
5. Integration of database into website environment

It is likely that the processes are going to be iterative, and backtracking can occur frequently. The order suggests a loose dependency between steps
   
**Why schema first?**

Knowing and designing a good schema early on is quite important. The schema outlines the database itself - without schema, I don’t know what tabbles to put in the database. 

On the other hand, relational schemas tend to organize data in unnatural (normalized) ways - at least that’s how I wanna do it. 

Data collection and insertion into the database can be made easier if we know what to look for. A schema serves as a guide. 

On the other hand, any collected data and insights drawn from the data can help inform schema development.



