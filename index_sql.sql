use sakila;
create table tes100 as select actor_id , first_name from actor where actor_id between 1 and 10;
 -- when we cretae using select command we get no primary key of original table \
 select * from tes100; -- no primary key actor_id is primary key in actor table but not in it
 
 
 desc tes100;
 
 explain select * from tes100 where actor_id=5;
 -- it will take time because it will go in every row
 
 
 -- indexes 
 
 -- index are object which is used to access our data in a faster way rather than searching data
 -- types of index -- clustered index and non clustered index 
 -- clustered index -- in sorted format (ascending order ) -- for example primary key 
 
insert into tes100 values ('14','abc'),('13','def'),('11','aman'),('12','shubham');
alter table tes100 add primary key(actor_id);
alter table tes100 drop primary key;

-- we can have only one clusttered index in a table
-- non clusttered index -- it creates another column as a reference 
-- syntax -- 
create index indx1 on tes100(actor_id);
show index from tes100;

explain select * from tes100 where actor_id=5;
explain select * from tes100 where first_name='aman'; -- this is not index so it will search in entire 14 rows

insert into tes100 values(12,'abc');
insert into tes100 values(15,'abc');

show index from tes100;

explain select*from tes100 where actor_id=14;

drop index indx1 on tes100;
show index from tes100;

-- index on 2 column
create index indx_composite on tes100(actor_id,first_name);
 -- sequence matters in this index is considered only on what is written first , rest helps to filter better
-- if dont use first column than it will search on entire data 
show index from tes100;
explain select * from tes100 where first_name='abc'; -- it will search on entire 14 rows

insert into tes100 values(17,'JOHH');
insert into tes100 values(18,'JOHN');
insert into tes100 values(19,'JOHEI');
insert into tes100 values(20,'JOHEIY');
drop index indx_composite on tes100;
show index from tes100;

-- partial index -- creating indexin on partial ( subset of rows)
-- when we have to make on the name , name are many so storring them would cost so much storage 
-- so make it on the subset that is few charaters from start 
-- index not on entire column but only starting three character
create index index_3_chr on tes100(first_name(3));
explain select * from tes100 where first_name = 'JOHNNY';
explain select * from tes100 where first_name like 'JOH%';
explain select * from tes100 where first_name like 'abc%';

-- learning assignment 







