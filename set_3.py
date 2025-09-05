'''Programming Set 3

This assignment will develop your ability to manipulate data.
'''

def relationship_status(from_member, to_member, social_graph):
    '''Relationship Status.

    Let us pretend that you are building a new app.
    Your app supports social media functionality, which means that users can have
    relationships with other users.

    There are two guidelines for describing relationships on this social media app:
    1. Any user can follow any other user.
    2. If two users follow each other, they are considered friends.

    This function describes the relationship that two users have with each other.

    Please see "set_3_sample_data.py" for sample data. The social graph
    will adhere to the same pattern.

    Parameters
    ----------
    from_member: str
        the subject member
    to_member: str
        the object member
    social_graph: dict
        the relationship data

    Returns
    -------
    str
        "follower" if from_member follows to_member,
        "followed by" if from_member is followed by to_member,
        "friends" if from_member and to_member follow each other,
        "no relationship" if neither from_member nor to_member follow each other.
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    
    # Program checks if from_member is following to_member.
    if to_member in social_graph[from_member]["following"]:

        # If yes, then it checks if to_member is following from_member.
        if from_member in social_graph[to_member]["following"]:
            status = "friends"

        else:
            status = "follower"

    else:
        # If from_member is not following to_member, it checks if to_member is following from_member.
        if from_member in social_graph[to_member]["following"]:
            status = "followed by"
        
        else: 
            status = "no relationship"

    # The relationship status is returned.
    return status

def tic_tac_toe(board):
    '''Tic Tac Toe.

    Tic Tac Toe is a common paper-and-pencil game.
    Players must attempt to successfully draw a straight line of their symbol across a grid.
    The player that does this first is considered the winner.

    This function evaluates a tic tac toe board and returns the winner.

    Please see "set_3_sample_data.py" for sample data. The board will adhere
    to the same pattern. The board may by 3x3, 4x4, 5x5, or 6x6. The board will never
    have more than one winner. The board will only ever have 2 unique symbols at the same time.

    Parameters
    ----------
    board: list
        the representation of the tic-tac-toe board as a square list of lists

    Returns
    -------
    str
        the symbol of the winner or "NO WINNER" if there is no winner
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    
    # The dimentions of the board is computed for.
    board_size = len(board)

    # The default winner is no winner.
    winning_piece = 'NO WINNER'

    # If there's no winner, all the potential horizontal lines are checked.
    if winning_piece == 'NO WINNER':

        for horizontal_line in board:
            if len(set(horizontal_line)) == 1 and (len(horizontal_line) == board_size):
                winning_piece = horizontal_line[1]

    # If there's no winner, all the potential vertical lines are checked.
    if winning_piece == 'NO WINNER':

        for count in range(board_size):
            vertical_line = []
            vertical_line = list(value[count] for value in board)
            if len(set(vertical_line)) == 1 and (len(vertical_line) == board_size):
                winning_piece = vertical_line[1]

    # If there's no winner, the downward diagonal line is checked.
    if winning_piece == 'NO WINNER':

        downward_diagonal = []
        for count in range(board_size):
            downward_diagonal.append(board[count][count])
            if len(set(downward_diagonal)) == 1 and (len(downward_diagonal) == board_size):
                    winning_piece = downward_diagonal[1]

    # If there's no winner, the upward diagonal line is checked.
    if winning_piece == 'NO WINNER':

        upward_diagonal = []
        for count in reversed(range(board_size)):
            upward_diagonal.append(board[count][(board_size - 1 - count)])
            if len(set(upward_diagonal)) == 1 and (len(upward_diagonal) == board_size):
                    winning_piece = upward_diagonal[1]
    
    # If there is a straight line of blank spaces, it is considered a no winner.
    if winning_piece == '':
        winning_piece = 'NO WINNER'

    # The winning piece is returned.
    return winning_piece

def eta(first_stop, second_stop, route_map):
    '''ETA.

    A shuttle van service is tasked to travel along a predefined circlar route.
    This route is divided into several legs between stops.
    The route is one-way only, and it is fully connected to itself.

    This function returns how long it will take the shuttle to arrive at a stop
    after leaving another stop.

    Please see "set_3_sample_data.py" for sample data. The route map will
    adhere to the same pattern. The route map may contain more legs and more stops,
    but it will always be one-way and fully enclosed.

    Parameters
    ----------
    first_stop: str
        the stop that the shuttle will leave
    second_stop: str
        the stop that the shuttle will arrive at
    route_map: dict
        the data describing the routes

    Returns
    -------
    int
        the time it will take the shuttle to travel from first_stop to second_stop
    '''
    # Replace `pass` with your code.
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    
    # Necessary variables are declared.
    travel_time = stops = starting_stop = last_stop = 0

    # The number of stops are checked using the loop.
    for first, second in route_map:
        stops += 1

    # Program determines the first stop, final destination, and their locations on the route_map.
    for (first, second), counter in zip(route_map, range(stops)):

        # If the starting location and final destination are in the same stop, the travel time is found.
        if (first == first_stop) and (second == second_stop):
            travel_time = route_map[first, second]["travel_time_mins"]
        
        # Otherwise, it takes the for the first stop.
        elif (first == first_stop) and (second != second_stop):
            travel_time += route_map[first, second]["travel_time_mins"]
            starting_stop = counter

        # Then it takes the time for the final stop.
        elif (first != first_stop) and (second == second_stop):
            travel_time += route_map[first, second]["travel_time_mins"]
            last_stop = counter

    # Any potential connecting trips required are computed for, given the way stops are ordered.
    if ((starting_stop  + 1) != last_stop):
        if (starting_stop < last_stop):
            for (first1, second1), counter1 in zip(route_map, range(stops)):
                if (starting_stop < counter1) and (counter1 < last_stop):
                    travel_time += route_map[first1, second1]["travel_time_mins"]
        
        elif (starting_stop > last_stop):
            for (first1, second1), counter1 in zip(route_map, range(stops)):
                if (starting_stop > counter1) and (counter1 < last_stop):
                    travel_time += route_map[first1, second1]["travel_time_mins"]
                if (starting_stop < counter1) and (counter1 > last_stop):
                    travel_time += route_map[first1, second1]["travel_time_mins"]

    # The remaining travel time is returned.
    return travel_time