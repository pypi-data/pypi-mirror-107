from neo4j import GraphDatabase
import sys
def count_node(uri,user,pwd):
    try:
        driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
        connect=1
    except (ValueError,OSError) as e:
        sys.exit("check for hostname , username and password")
    if(connect==1):
        session=driver.session()
        count_query="""match (n) return count(n) as count"""
        count_result=session.run(count_query)
        for count in count_result:
            nodecount=count["count"]
        return nodecount
    