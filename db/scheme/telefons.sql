create table if not exists telefons (
       id mediumint auto_increment primary key,
       tlf varchar(9) not null,
       nom text CHARACTER SET 'utf8' not null,
       dept text CHARACTER SET 'utf8',
       tlf_dir varchar(9),
       email text,
       area text CHARACTER SET 'utf8'
)DEFAULT CHARSET=utf8;
