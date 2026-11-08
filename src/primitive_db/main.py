#!/usr/bin/env python3
from primitive_db.engine import run


def main():
    run()


if __name__ == "__main__":
    main()


"""create_table users name:str age:int is_active:bool

insert into users values ("Sergei", 28, true)

insert into users values ("Anna", 22, false)

select from users

select from users where age = 28

update users set age = 29 where name = "Sergei"

delete from users where name = "Anna"

info users"""
