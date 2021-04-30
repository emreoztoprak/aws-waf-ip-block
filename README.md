# AWS-WAF-IP-Block

![alt text](https://miro.medium.com/max/1400/1*IOcM-EMBBW4N-fLxgDK9zg.jpeg)

First of all to do this, you must have enabled the Waf logging and then created a table from these logs in the Athena.

Two AWS documentation explaining how to do these operations.

https://docs.aws.amazon.com/waf/latest/developerguide/logging.html

https://docs.aws.amazon.com/athena/latest/ug/waf-logs.html

Now we can query our waf logs on Athena. This query will give us IP addresses whose requests have been blocked more than 100 times.

    SELECT httpRequest.clientIp,
    COUNT (*) count
    FROM waf_logs
    WHERE action='BLOCK'
    GROUP BY httpRequest.clientIp
    HAVING COUNT(*) > 100
    ORDER BY count DESC
    
 Another thing is that you have to create an IP set and add it to the web acl. After you can use this ip set in the lambda function.
 
 
 
 https://engineering.teknasyon.com/blocking-malicious-ip-using-aws-waf-2e5c4ed2defb
