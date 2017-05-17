create table if not exists telefons (
       id mediumint auto_increment primary key,
       tlf varchar(9) not null,
       nom text CHARACTER SET 'utf8' not null
)DEFAULT CHARSET=utf8;
