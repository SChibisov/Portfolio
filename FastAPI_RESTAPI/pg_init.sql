create table public.users (
    id serial primary key,
    login varchar(100),
    email varchar(100),
    age integer
);

create table public.products (
    id serial primary key,
    product_name varchar(100),
    product_cnt integer,
    is_available boolean
);

create table public.carts (
    id serial primary key,
    user_id integer,
    product_id integer,
    product_count integer
);


insert into public.users (login, email, age) values ('nick', 'nick@mail.com', 20), ('moose', 'moose@mail.com', 30);
insert into public.products (product_name, product_cnt, is_available) values ('Стол', 10, true), ('Стул', 100, true);
insert into public.carts (user_id, product_id, product_count) values (3, 2, 3);


select carts.id, carts.user_id, carts.product_id, products.product_name, carts.product_count from public.carts AS carts
left join public.products products on carts.product_id = products.id
where user_id=3;




select * from users;
select * from public.products
