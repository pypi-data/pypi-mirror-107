def getCompleteness(connectionMap, attribute, grouping= []):
        try:
            groupValue = ''
            groupLogic = ''
            orderLogic = ''
            for item in grouping:
                groupValue = groupValue + item + ','
            if len(grouping) > 0:
                # Create specific SQL statement and remove last ","
                groupLogic = 'GROUP BY ' + groupValue[:-1]
                orderLogic = 'ORDER BY ' + groupValue[:-1]
                # Enter sql logic values to connecitonMap
                connectionMap.update({'attribute': attribute, 'groupValue': groupValue, 'groupLogic': groupLogic,
                                      'orderLogic': orderLogic})
                SQLQuery="""
                SELECT 
                A.* ,
                (ISNULL(A.No_Of_EMPTY,0)+ISNULL(A.No_Of_NA,0)+ISNULL(A.No_Of_NULL,0)) AS Total_Missing_Val ,
                (cast((ISNULL(A.No_Of_EMPTY,0)+ISNULL(A.No_Of_NA,0)+ISNULL(A.No_Of_NULL,0)) as float))/A.CountRows as Per_Missing_val
                FROM
                (
                SELECT
                {groupValue}
                SUM( CASE WHEN TRY_CONVERT(CHAR ,{attribute})='' THEN 1 ELSE NULL END )AS No_Of_EMPTY ,
                SUM( CASE WHEN TRY_CONVERT(CHAR ,{attribute})= 'NA' THEN 1 ELSE NULL END ) AS No_Of_NA ,
                SUM( CASE WHEN {attribute} IS NULL THEN 1 ELSE NULL END) AS No_Of_NULL,
                count(*) as CountRows
                
                FROM {schema}.{table}
                {groupLogic}                 
                )A
                {orderLogic}
                """.format(**connectionMap)
                # format(schema, table, attribute, groupValue, groupLogic, orderLogic)
            return SQLQuery
        except Exception as e:
            e.args = e.args + ('Check if name {0} is present in input dataset'.format(e.args),)
            raise
                                
