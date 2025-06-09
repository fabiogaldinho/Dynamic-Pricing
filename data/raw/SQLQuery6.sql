SELECT I.Qtde as quantity_out, I.DataInc as date_out, P.Hora as time_out
FROM Pedite as I
LEFT JOIN pedido as P on I.Nrodoc = P.Nrodoc
WHERE I.Calitem = 40
	AND I.DataInc >= '2024-01-01'
	AND P.CaixaSN = 'S'
ORDER BY DataInc ASC, Hora ASC;