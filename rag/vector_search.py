import pymongo
import utils

def recall(
    self, text, n_docs=2, min_rel_score=0.25, chunk_max_length=800, unique=True
):
    """
    Retrieves relevant documents from the knowledge base based on a query.

    This function uses MongoDB's $vectorSearch aggregation stage to find documents
    with vector embeddings similar to the query embedding. It then filters and
    formats the results.

    The optimization moves the uniqueness check from the client-side Python code
    to the database aggregation pipeline. This is more efficient as the database
    can perform this operation much faster than Python.

    - Original approach: Fetched 15 documents, then looped in Python to find
      unique sources until `n_docs` was reached.
    - Optimized approach: Uses a `$group` stage in the MongoDB pipeline to get
      unique documents by "source" directly from the database, then limits
      the result to `n_docs`.
    """
    utils.print_log("recall (VectorSearch)=>" + str(text))

    try:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "default",
                    "queryVector": self.gpt4all_embd.embed_query(text),
                    "path": "embedding",
                    "limit": 15,
                    "numCandidates": 50,
                }
            },
            {"$addFields": {"score": {"$meta": "vectorSearchScore"}}},
            {"$match": {"score": {"$gte": min_rel_score}}},
        ]
        if unique:
            pipeline.extend(
                [
                    # Optimization: Group by source to get unique documents
                    # This is more efficient than client-side filtering
                    {"$group": {"_id": "$source", "docs": {"$first": "$$ROOT"}}},
                    {"$replaceRoot": {"newRoot": "$docs"}},
                ]
            )
        # Limit the number of documents returned
        pipeline.append({"$limit": n_docs})
        pipeline.append({"$project": {"score": 1, "_id": 0, "source": 1, "text": 1}})
        response = self.collection.aggregate(pipeline)

    except pymongo.errors.OperationFailure as ex:
        err_type = type(ex).__name__
        err_args = ex.args
        message = f"<b>Error! Please verify Atlas Search index exists.</b><hr/> An exception of type {err_type} occurred with the following arguments:\n{err_args}"
        self.st.write(f"<div>{message}</div>", unsafe_allow_html=True)
        raise
    except Exception as ex:
        err_type = type(ex).__name__
        err_args = ex.args
        message = f"<b>Error! An exception of type {err_type} occurred with the following arguments:\n{err_args}"
        self.st.write("<div>{message}</div>", unsafe_allow_html=True)
        raise

    tmp_docs = []
    str_response = []

    # Iterate over the results
    for d in response:
        tmp_docs.append(d["source"])
        str_response.append(
            {
                "URL": d["source"],
                "content": d["text"][:chunk_max_length],
                "score": d["score"],
            }
        )
        kb_output = (
            f"RAG Knowledgebase Results[{len(tmp_docs)}]:\n```{str(str_response)}```\n## \n```SOURCES: "
            + str(tmp_docs)
            + "```\n\n"
        )
        self.st.write(kb_output)
        return str(kb_output)