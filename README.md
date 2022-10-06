# ecommerce-api
<h1> A Basic E-Commerce API using TDD. </h1>

<h3> Steps to get the project on your computer: </h3>

## Create a directory where you want to clone the project
`````shell script
mkdir ecom
`````

## Change into the directory
`````shell script
cd ecom
`````

## clone the project
`````shell script
git clone https://github.com/simofirdoussi/ecommerce-api.git
`````

**Build locally and run**

## Build the Docker image
`````shell script
docker-compose build
`````

## Start the development server
`````shell script
docker-compose run --rm app sh -c "python manage.py runserver"
`````

**Important:**

Adding the necessary packages to the requirements.txt or requirements.dev.txt(for dev only packages) file is necessary before any push.
After the push, a series of checks are run automatically(see .github/worflows/checks.yml), including flake8 and the unit tests. Please make sure to format your code before pushing to the repository.
Flake8 which is a great toolkit for checking your code base against coding style (PEP8), programming errors (like “library imported but unused” and “Undefined name”).
