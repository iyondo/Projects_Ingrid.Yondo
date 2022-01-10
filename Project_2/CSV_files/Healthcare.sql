create database healthcare; 

use healthcare;

create table world (country_name varchar(255), ISO varchar(255), Region varchar(255));
create table cases (country_name varchar(255), total_cases int, new_cases int, total_deaths int, total_recoveries int, new_recoveries int, active_cases int, serious_critical int);
create table vaccination (country_name varchar(255), total_vaccinations int, people_vaccinated_1 int, people_fully_vaccinated int);
create table development (Country varchar(255), population float, life_expectency float, HDI float);


#Queries
#1 - The country with the most deaths
SELECT Country_name, max(TotalDeaths) 
FROM healthcare.cases;

#2 - Number of people fully vaccinated in Germany:
SELECT Country_name, People_fully_vaccinated 
FROM healthcare.vaccination
WHERE Country_name = "Germany";

#3 -  Number of deaths for the top 5 countries with low life expectancy:
SELECT Dvlp.Country_name, Dvlp.life_expectancy, cases1.TotalDeaths
FROM healthcare.development  Dvlp
LEFT JOIN healthcare.cases cases1
ON Dvlp.Country_name = cases1.Country_name
WHERE SeriousCritical IS NOT NULL
GROUP BY Dvlp.Country_name
ORDER BY Dvlp.life_expectancy ASC;

