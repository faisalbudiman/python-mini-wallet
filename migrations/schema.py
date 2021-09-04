from sqlalchemy import create_engine, text
from os import environ

engine = create_engine(environ.get('DATABASE_URI_DEV'))

with engine.connect() as conn:
    conn.execute(text(
        """
            DROP TABLE IF EXISTS user ;
        """
    ))
    conn.execute(text(
        """
        CREATE TABLE `user` (
            `id` VARCHAR(100) NOT NULL UNIQUE,
            PRIMARY KEY (`id`)
        )
        ENGINE=InnoDB
        ;
        """
    ))
    conn.execute(text(
        """
            DROP TABLE IF EXISTS user_balance ;
        """
    ))
    conn.execute(text(
        """
        CREATE TABLE `user_balance` (
            `id` VARCHAR(100) NOT NULL UNIQUE,
            `user_id` VARCHAR(100) NOT NULL,
            `balance` INT(11) NOT NULL,
            `last_transaction_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            `status` ENUM('enabled', 'disabled') NOT NULL DEFAULT 'disabled',
            `enabled_at` TIMESTAMP NULL,
            `disabled_at` TIMESTAMP NULL,
            PRIMARY KEY (`id`),
            INDEX `user_id` (`user_id`)
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    ))
    conn.execute(text(
        """
            DROP TABLE IF EXISTS user_balance_history ;
        """
    ))

    conn.execute(text(
        """
        CREATE TABLE `user_balance_history` (
            `id`  VARCHAR(100) NOT NULL UNIQUE,
            `user_balance_id` VARCHAR(100) NOT NULL,
            `amount` INT(11) NOT NULL,
            `reference_id` VARCHAR(100) NOT NULL UNIQUE,
            `balance_before` INT(11) NOT NULL,
            `balance_after` INT(11) NOT NULL,
            `type` ENUM('debit','credit') NOT NULL,
            `transaction_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (`id`),
            INDEX `user_balance_id` (`user_balance_id`)
        )
        COLLATE='latin1_swedish_ci'
        ENGINE=InnoDB
        ;
        """
    ))

    print("success..")