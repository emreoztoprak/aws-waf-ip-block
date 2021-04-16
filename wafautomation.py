import boto3
from threading import Event

def lambda_handler(event, context):

    wafclient = boto3.client('wafv2')

    wafresult = wafclient.get_ip_set(
        Name='blocked-ip',
        Scope='REGIONAL',
        Id='YOUR IP SET ID'
    )
    token = wafresult['LockToken']

    athenaclient=boto3.client('athena')

    QUERY_STR="""
    SELECT httpRequest.clientIp,
    COUNT (*) count
    FROM waf_logs
    WHERE action='BLOCK'
    GROUP BY httpRequest.clientIp
    HAVING COUNT(*) > 100
    ORDER BY count DESC
    """
    response = athenaclient.start_query_execution(
        QueryString=QUERY_STR,
        QueryExecutionContext={'Database': 'default'},
        ResultConfiguration={'OutputLocation': 's3://YOUR-ATHENA-QUERY-OUTPUT'}
    )
    queryid = response['QueryExecutionId']


    Event().wait(15)
    #I added this command to wait for the query to finish.
    result = athenaclient.get_query_results(QueryExecutionId=queryid)

    data = result['ResultSet']['Rows']
    data.pop(0)
    iplist=[]
    for item in data:
        iplist.append(item['Data'][0]['VarCharValue']+'/32')


    print(iplist)
    response = wafclient.update_ip_set(
            Name='blocked-ip',
            Scope='REGIONAL',
            Id='YOUR IP SET ID',
            Description='bloklanan ip adresleri',
            Addresses=iplist,
            LockToken=token
        )
    return response
