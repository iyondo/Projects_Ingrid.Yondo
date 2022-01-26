CREATE DATABASE Project3;
USE Project3;
SELECT * FROM project_dataframe;


SELECT Id, IsCyberbullying_encode FROM Project3.project_dataframe;

SELECT Id, COUNT(IsCyberbullying_encode)
FROM Project3.project_dataframe
WHERE IsCyberbullying_encode = 1;

SELECT Id, COUNT(IsCyberbullying_encode)
FROM Project3.project_dataframe;

SELECT AVG(`SlangWords#`) 
FROM project_dataframe;

SELECT AVG(AvgWordLength) 
FROM project_dataframe
WHERE IsCyberbullying_encode = 1;

SELECT AVG(SenderFollowings) 
FROM Project3.project_dataframe;

SELECT AVG(SenderFollowers) 
FROM Project3.project_dataframe;
    
    
    



