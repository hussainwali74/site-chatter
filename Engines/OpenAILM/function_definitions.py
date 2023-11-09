functions=[
    {
        "name":"post_creator",
        "description":"use this function to post blog to wordpress",
        "parameters":{
            "type":"object",
            "properties":{
                "title":{
                    "type":"string",
                    "description":"Title of the blog post. Do not guess. Do not make something up. If unkown return -1."
                },
                "content":{
                    "type":"string",
                    "description":"Content of the blog post. Do not guess. Do not make something up. If unkown return -1."
                },
            },
            "required":["title","content"]
        }
    }
]