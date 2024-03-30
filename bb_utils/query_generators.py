from spider_inputs import google_search_queries, team_names, player_names

def generate_queries():
    generated_queries = []

    for query in google_search_queries:
        if "{team_name}" in query:
            for team_name in team_names:
                generated_query = query.replace("{team_name}", team_name)
                generated_queries.append(generated_query)
        elif "{player_name}" in query:
            for player_name in player_names:
                generated_query = query.replace("{player_name}", player_name)
                generated_queries.append(generated_query)
        else:
            generated_queries.append(query)

    return generated_queries
