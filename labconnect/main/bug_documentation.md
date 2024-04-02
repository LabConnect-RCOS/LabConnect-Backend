## Bugs that need to be resolved

### Operational Error: sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) ambiguous column name: opportunities.id

#### Things We've Attempted & Ruled out

- make & make develop not working
- the column opportunities.id doesn't exist
- db doesn't exist
- new db object (aka it's a different db object)
- 


## Fixed Bugs

### AssertionError: applications must write bytes

 - replaced Opportunities.name with just Opportunities
 (call whole table instead of individual columns)