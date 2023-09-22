Database management systems are specialized software to store and manage large scale data, and provides the ability to query data with optimized algorithms, and more.

2 main types of databases: relational and non-relational. 

**About relational databases and schemas**
One key distinction between them is that relational databases have a schema, which outlines the relations of the database. In other words, the schema is just the collection of tables, with all the attributes (columns) the database will have. Schemas offer guarantees, but it requires careful design to be effective. 

**Why relational databases for us?**
We imagine that our product prioritizes accuracy - students and researchers need the right connections. The emphasis is on the matching of people to projects. I think relational databases will serve us well regarding our priority.

How the database will be designed and implemented
1. Discuss with potential users about the data they’d expect the system to have, to yield a natural description of the data needs.
2. Draw an ER Diagram of the data based on the natural description.
3. Devise database schema from ER Diagram
4. Database implementation
5. Develop commonly used queries based on use cases collected by the project.
6. Database testing: data insertion and querying.
7. Integration of database into website environment
   
**Why schema first?**
Knowing and designing a good schema early on is quite important. On one hand, besides the benefits of schemas, the schema outlines the database itself - without schema, I don’t know what to put in the database. On the other hand, relational schemas tend to organize data in unnatural (normalized) ways - at least that’s how I wanna do it - and thus data collection and insertion into the database can be made easier if we know what to look for. 

