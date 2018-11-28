Part 1: Files Description

SimpleFlask.py:		Simple Flask implement
SimpleBO.py: 		Simple BO implement (POST, PUT, GET, DELETE)
Query.py:		Custom query functions
/screenshots:		Screenshots for test cases (test cases provided in Part 2)
/Queries:
  /create queries:	Create Statements for six tables (I mainly did some cleanup for fielding table)
  /Schema_Modification.sql:	Schema Modification statements I used to modify the original schema
  /custom queries:	Custom Queries Statements (also shown in Query.py)


Part 2: Test cases (Results are in /screenshots)
TC1: GET http://localhost:5000/api/people?nameLast=Smith&fields=nameLast,playerID
TC2: GET http://localhost:5000/api/people?nameLast=Smith&fields=nameLast,playerID&offset=10&limit=10
TC3 (last page of result so no “next” link): GET http://localhost:5000/api/people?nameLast=Smith&fields=nameLast,playerID&offset=150&limit=10
TC4 (body provided in screenshot): POST http://localhost:5000/api/people
TC5 (after doing TC4 by posting a fake data “willite02”): GET http://localhost:5000/api/people/willite02
TC6 (body provided in screenshot): PUT http://localhost:5000/api/people/willite02
TC7: DELETE http://localhost:5000/api/people/willite02
TC8 (after doing TC7 by deleting the fake data “willite02”): GET http://localhost:5000/api/people/willite02
TC9: GET http://localhost:5000/api/batting/borlato01_1960_1/people?fields=nameFirst,nameLast
TC10 (body provided in screenshot, it will raise duplicate key error): POST http://localhost:5000/api/people/willite01/batting
TC11: GET http://localhost:5000/api/teammates/willite01
TC12: GET http://localhost:5000/api/teammates/willite01?offset=10&limit=10
TC13: GET http://localhost:5000/api/people/willite01/career_stats
TC14: GET http://localhost:5000/api/roster?teamid=BOS&yearid=2004
