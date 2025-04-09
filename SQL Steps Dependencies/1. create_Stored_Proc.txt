USE [SQLTEST] -- Database name
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE PROCEDURE [dbo].[SP_Step_Execution_Order]
    @UNIT_NBR INT
AS
BEGIN
    SET NOCOUNT ON;

    WITH StepExecution ( --to compute the [execution order] based on step_seq and step_dep
		UNIT_NBR, 
		STEP_SEQ_ID, 
		STEP_DEP_ID, 
		execution_order
	) 
	AS (
		SELECT --to establish the first step to start being the step_seq with no dependecies
			UNIT_NBR,
			STEP_SEQ_ID,
			STEP_DEP_ID,
			1 AS execution_order
		FROM dbo.DEPENDENCY_RULES
		WHERE STEP_DEP_ID = 0
			AND UNIT_NBR = @UNIT_NBR

		UNION ALL

		SELECT 
			dr.UNIT_NBR,
			dr.STEP_SEQ_ID,
			dr.STEP_DEP_ID,
			se.execution_order + 1
		FROM dbo.DEPENDENCY_RULES dr
			INNER JOIN StepExecution se ON -- to enable recursive join
				dr.UNIT_NBR = se.UNIT_NBR 
				AND dr.STEP_DEP_ID = se.STEP_SEQ_ID
		WHERE dr.UNIT_NBR = @UNIT_NBR
	),

	FinalExecution AS (
		SELECT 
			UNIT_NBR,
			STEP_SEQ_ID,
			MAX(execution_order) AS execution_order --select the highest [execution order] based on each step_seq
		FROM StepExecution
		GROUP BY UNIT_NBR, STEP_SEQ_ID
	)

	SELECT 
		fe.UNIT_NBR,
		fe.STEP_SEQ_ID,
		pn.STEP_PROG_NAME,
		fe.execution_order
	FROM FinalExecution fe
		LEFT JOIN dbo.PROG_NAME pn ON --to join the step_name for better readability
			pn.UNIT_NBR = @UNIT_NBR
			AND fe.STEP_SEQ_ID = pn.STEP_SEQ_ID
	ORDER BY fe.execution_order
	OPTION (MAXRECURSION 500); --to avoid the default 100 recursion limit

END
GO


