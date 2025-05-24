SELECT Qtde as quantity_in, DataInc as date_in
FROM EntradaIte
WHERE Materia = 40 AND Datainc >= '2024-01-01'
ORDER BY Datainc ASC;