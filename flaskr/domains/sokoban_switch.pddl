(define (domain tricky_sokoban)

	(:requirements
		:typing
	)

	(:types
        cell_x cell_y box
	)

	
	(:predicates
	    (player_at ?C - cell_x ?R - cell_y)
	    (box_at ?b - box ?C - cell_x ?R - cell_y)
	    (switch_at ?C - cell_x ?R - cell_y)
	    (switch_activated)
        (free_cell ?C - cell_x ?R - cell_y)
        (increasing_x ?C1 - cell_x ?C2 - cell_x)
        (increasing_y ?R1 - cell_y ?R2 - cell_y)
	)


	(:action move_right
		:parameters (?C1 - cell_x ?R1 - cell_y ?C2 - cell_x )
		:precondition (and (player_at ?C1 ?R1) (free_cell ?C2 ?R1) (increasing_x ?C2 ?C1))
		:effect (and (player_at ?C2 ?R1) (free_cell ?C1 ?R1)  (not (player_at ?C1 ?R1)) (not (free_cell ?C2 ?R1) ))
	)
	
	(:action move_left
		:parameters (?C1 - cell_x ?R1 - cell_y ?C2 - cell_x )
		:precondition (and (player_at ?C1 ?R1) (free_cell ?C2 ?R1) (increasing_x ?C1 ?C2))
		:effect (and (player_at ?C2 ?R1) (free_cell ?C1 ?R1)  (not (player_at ?C1 ?R1)) (not (free_cell ?C2 ?R1) ))
	)
	
	(:action move_up
		:parameters (?C1 - cell_x ?R1 - cell_y ?R2 - cell_y )
		:precondition (and (player_at ?C1 ?R1) (free_cell ?C1 ?R2) (increasing_y ?R2 ?R1))
		:effect (and (player_at ?C1 ?R2) (free_cell ?C1 ?R1)  (not (player_at ?C1 ?R1)) (not (free_cell ?C1 ?R2) ))
	)
	
	(:action move_down
		:parameters (?C1 - cell_x ?R1 - cell_y ?R2 - cell_y )
		:precondition (and (player_at ?C1 ?R1) (free_cell ?C1 ?R2) (increasing_y ?R1 ?R2))
		:effect (and (player_at ?C1 ?R2) (free_cell ?C1 ?R1)  (not (player_at ?C1 ?R1)) (not (free_cell ?C1 ?R2) ))
	)
	
	(:action push_box_right
		:parameters (?b - box ?C1 - cell_x ?R1 - cell_y ?C2 - cell_x ?C3 - cell_x)
		:precondition (and (switch_activated) (player_at ?C1 ?R1) (box_at ?b ?C2 ?R1) (free_cell ?C3 ?R1) (increasing_x ?C3 ?C2) (increasing_x ?C2 ?C1))
		:effect (and (player_at ?C2 ?R1) (free_cell ?C1 ?R1) (box_at ?b ?C3 ?R1) (not (player_at ?C1 ?R1)) (not (box_at ?b ?C2 ?R1)) (not (free_cell ?C3 ?R1) ))
	)
	
	(:action push_box_left
		:parameters (?b - box ?C1 - cell_x ?R1 - cell_y ?C2 - cell_x ?C3 - cell_x)
		:precondition (and (switch_activated) (player_at ?C1 ?R1) (box_at ?b ?C2 ?R1) (free_cell ?C3 ?R1) (increasing_x ?C2 ?C3) (increasing_x ?C1 ?C2))
		:effect (and (player_at ?C2 ?R1) (free_cell ?C1 ?R1) (box_at ?b ?C3 ?R1) (not (player_at ?C1 ?R1)) (not (box_at ?b ?C2 ?R1)) (not (free_cell ?C3 ?R1) ))
	)
	
	(:action push_box_up
		:parameters (?b - box ?C1 - cell_x ?R1 - cell_y ?R2 - cell_y ?R3 - cell_y)
		:precondition (and (switch_activated) (player_at ?C1 ?R1) (box_at ?b ?C1 ?R2) (free_cell ?C1 ?R3) (increasing_y ?R3 ?R2) (increasing_y ?R2 ?R1))
		:effect (and (player_at ?C1 ?R2) (free_cell ?C1 ?R1) (box_at ?b ?C1 ?R3) (not (player_at ?C1 ?R1)) (not (box_at ?b ?C1 ?R2)) (not (free_cell ?C1 ?R3) ))
	)
	
	(:action push_box_down
		:parameters (?b - box ?C1 - cell_x ?R1 - cell_y ?R2 - cell_y ?R3 - cell_y)
		:precondition (and (switch_activated) (player_at ?C1 ?R1) (box_at ?b ?C1 ?R2) (free_cell ?C1 ?R3) (increasing_y ?R2 ?R3) (increasing_y ?R1 ?R2))
		:effect (and (player_at ?C1 ?R2) (free_cell ?C1 ?R1) (box_at ?b ?C1 ?R3) (not (player_at ?C1 ?R1)) (not (box_at ?b ?C1 ?R2)) (not (free_cell ?C1 ?R3) ))
	)
	
	(:action activate_switch
		:parameters (?C1 - cell_x ?R1 - cell_y)
		:precondition (and (player_at ?C1 ?R1) (switch_at ?C1 ?R1))
		:effect (and (switch_activated))
	)
)