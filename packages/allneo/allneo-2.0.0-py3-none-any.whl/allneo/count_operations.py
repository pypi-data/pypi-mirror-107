from neo4j import GraphDatabase
def count_node(uri,user,pwd):
    try:
        driver=GraphDatabase.driver(uri=uri,auth=(user,pwd))
        connect=1
    except Exception as e:
        connect=0
        error=e
    if(connect==0):
        print(error)
    else:
        session=driver.session()
        count_query="""match (n) return count(n) as count"""
        count_result=session.run(count_query)
        for count in count_result:
            nodecount=count["count"]
        return nodecount
    