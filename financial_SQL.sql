SELECT * FROM financial_inclusion_project_schema.financial_inclusion_dataset_new;

#	Count users per country.
SELECT country, COUNT(*) AS user_count
FROM financial_inclusion_project_schema.financial_inclusion_dataset_new
GROUP BY country
ORDER BY user_count DESC;

# Average income per education level.
SELECT education_level, 
       AVG(monthly_income) AS average_income
FROM financial_inclusion_project_schema.financial_inclusion_dataset_new
GROUP BY education_level
ORDER BY average_income DESC;

#	Correlate bank account ownership with mobile money usage.
SELECT 
    has_bank_account,
    mobile_money_user,
    COUNT(*) AS user_count
FROM financial_inclusion_project_schema.financial_inclusion_dataset_new
GROUP BY 
   has_bank_account,
    mobile_money_user
ORDER BY 
     has_bank_account,
    mobile_money_user; 
 
#	Segment users by financial inclusion status.
    SELECT 
    CASE
        WHEN has_bank_account = 'Yes' AND mobile_money_user = 'Yes'
            THEN 'Fully Included'
        WHEN has_bank_account = 'Yes' OR mobile_money_user = 'Yes'
            THEN 'Partially Included'
        ELSE 'Excluded'
    END AS financial_inclusion_status,
    COUNT(*) AS user_count
FROM financial_inclusion_project_schema.financial_inclusion_dataset_new
GROUP BY financial_inclusion_status;
