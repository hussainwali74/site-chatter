from pymongo import MongoClient

async def count_records(collection, filter_query=None):
    print('--------------------------------------');
    print('filtery_query=',filter_query);
    print('--------------------------------------');
    
    """Takes a collection and queries the collection by filter_query returns count of docs in the collection"""
    if filter_query:
        count = await collection.count_documents(filter_query)
    else:
        count = await collection.estimated_document_count()

    return count
