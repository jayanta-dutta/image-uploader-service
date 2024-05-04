# Set up PostgresSQL database locally

* (This steps are for mac user, and for windows and linux user respective steps apply)
* Step 1: Install homebrew
       /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
* Step 2: Install PostgreSQL
Once Homebrew is installed, you can use it to install PostgreSQL. Run the following command in your terminal:
brew install postgresql
* Step 3: Start PostgreSQL Service:
brew services start postgresql
* Step 4: Set Up PostgreSQL
connect to PostgreSQL using the psql command-line tool: psql postgres

* Set Up a Database and User 

You might want to create a separate database and user for your application. You can do this within the psql shell:

    CREATE DATABASE your_database_name;
    CREATE USER your_username WITH ENCRYPTED PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;

Replace your_database_name, your_username, and your_password with your preferred values.

* --- create schema--


    CREATE SCHEMA mywork;
    GRANT ALL ON SCHEMA mywork TO postgres_user;

* Create table 


    CREATE TABLE mywork.images (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        image_data BYTEA
    );