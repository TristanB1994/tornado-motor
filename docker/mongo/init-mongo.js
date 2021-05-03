db.getSiblingDB('registry');
db.createUser({ user: 'dba',pwd: 'password',roles: ["root"]});
db.start.insertOne({'name':'db_primer'});
