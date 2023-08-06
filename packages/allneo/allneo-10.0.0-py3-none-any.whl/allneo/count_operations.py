from neo4j import GraphDatabase
import sys
def count_node(uri,user,pwd):
    connect=0
    try:
        driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
        connect=1
    except Exception as error:
        print(error)
        sys.exit(0)
    if(connect==1):
        session=driver.session()
        count_query="""match (n) return count(n) as count"""
        count_result=session.run(count_query)
        for count in count_result:
            nodecount=count["count"]
        return nodecount
    else:
        print("please check your hostname , userid and password")
    