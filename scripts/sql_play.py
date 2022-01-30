import time
import pandas as pd
import sqlalchemy


def execute_query(sql, cxn):
    start_time = time.time()
    res = pd.read_sql("set arithabort on; " + sql, cxn)
    elapsed_time = time.time() - start_time
    print(f"Executed in {elapsed_time} S")
    return res


engine = sqlalchemy.create_engine(
    'mssql+pyodbc://sa:dev@(local)/Operations?driver=ODBC+Driver+17+for+SQL+Server',
    connect_args={'autocommit': True}
)

cxn = engine.connect()

sql = """
     select
            usage_type,     
            sum(line_item_blended_cost) as line_item_blended_cost
        from (
                select
                    month,
                    case 
                        when line_item_usage_type in (
                            'EUW2-BoxUsage:t2.large',
                            'EUW2-EBS:VolumeUsage.gp2',
                            'EUW2-BoxUsage:t3.medium',
                            'EUW2-DataTransfer-Out-Bytes',
                            'EUW2-EBS:SnapshotUsage',
                            'EUW2-BoxUsage:t3.micro',
                            'EUW2-ElasticIP:IdleAddress') then line_item_usage_type
                        else 'Other' end as usage_type,
                        line_item_blended_cost
                    from aws_cur_data
                    where line_item_product_code= 'AmazonEC2'     
            ) t
        where 
            month = 10
            and line_item_blended_cost <> 0
        group by 
              usage_type
        order by 
            line_item_blended_cost desc
"""

df = execute_query(sql, cxn)
