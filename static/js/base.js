// creates game event
function createTimeSlot() {
	var postVars = $('#create_event :input:not(:checkbox), #create_event :input:checkbox:checked').serialize();
	$.post('/services/events/create', postVars,
		function(response) {
			if(response.error) {
				$("#create_form").after("<tr><td colspan=6>Error occured while saving timeslot: " + response.error + "</td></tr>");
			} else {
				$("#create_form").after("<tr><td>Time Slot:</td><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td colspan=2>" + response.date + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // createTimeSlot()

// edits game event
function editTimeSlot() {
	alert("Not implemented yet");
	return false;
} // editTimeSlot()

//saves a goal record
function saveGoal() {
	if(!$('#goal_player').val()) {
		alert("Please provide goal player number.");
		return false;
	}
	if(!$('#goal_time_minute').val()) {
		alert("Please provide goal minute.");
		return false;
	}
	if(!$('#goal_time_second').val()) {
		alert("Please provide goal second.");
		return false;
	}	
	if(isNaN($('#goal_player').val()) || $('#goal_player').val() < 0 ) {
		alert("Invalid player number.");
		return false;
	}	
	if(isNaN($('#goal_time_minute').val()) || $('#goal_time_minute').val() < 0 || $('#goal_time_minute').val() > 59 ) {
		alert("Invalid goal minute.");
		return false;
	}		
	if(isNaN($('#goal_time_second').val()) || $('#goal_time_second').val() < 0 || $('#goal_time_second').val() > 59 ) {
		alert("Invalid goal second.");
		return false;
	}		
	var postVars = $('#event_id, #goals :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventgoals/create', postVars,
		function(response) {
			if(response.error) {
				$("#goals").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#goals").after("<tr id='goal_object_" + response.goal_id + "'><td>" + response.team + "</td><td>" +
					response.player + "</td><td>" + response.period + 
					"</td><td>" + response.time_minute + ":" + response.time_second + "</td>" +
					"<td><input type='button' name='edit_goal' id='edit_goal' value='Edit' onClick='editGoal(" + response.goal_id + ")'/> " +
					"<input type='button' name='delete_goal' id='delete_goal' value='Delete' onClick='deleteGoal(" + response.goal_id + ")'/></td></tr>");
				$('#goal_player').val(null);
				$('#goal_period').val(1);
				$('#goal_time_minute').val(null);
				$('#goal_time_second').val(null);
			}
		}, "json"
	);
	return false;
} // saveGoal()

function editGoal(id) {
	$.post('/services/eventgoals/detail', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to edit goal.");
			} else {
				deleteGoal(id);
				$('#goal_team').val(response.team);
				$('#goal_player').val(response.player);
				$('#goal_period').val(response.period);
				$('#goal_time_minute').val(response.time_minute);
				$('#goal_time_second').val(response.time_second);
			}
		}, "json"
	);
	return false;
} // editGoal()

function deleteGoal(id) {
	$.post('/services/eventgoals/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to delete goal.");
			} else {
				$('#goal_object_'+id).remove();
			}
		}, "json"
	);
	return false;
} // deleteGoal()

function savePenalty() {
	var postVars = $('#event_id, #penalties :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventpenalties/create', postVars,
		function(response) {
			if(response.error) {
				$("#penalties").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#penalties").after("<tr><td>Time Slot:</td><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td colspan=2>" + response.date + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // savePenalty()

function deletePenalty(id) {
	$.post('/services/eventpenalties/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to delete penalty.");
			} else {
				$('#goal_object_'+id).remove();
			}
		}, "json"
	);
} // deletePenalty()

function saveSuspension() {
	var postVars = $('#event_id, #suspensions :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventsuspensions/create', postVars,
		function(response) {
			if(response.error) {
				$("#suspensions").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#suspensions").after("<tr><td>Time Slot:</td><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td colspan=2>" + response.date + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // saveSuspension()

function deleteSuspension(id) {
	$.post('/services/eventsuspensions/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to delete penalty.");
			} else {
				$('#goal_object_'+id).remove();
			}
		}, "json"
	);
} // deleteSuspension()

function saveGoalkeeperSaves() {
	var postVars = $('#event_id, #saves :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventgoalkeepersaves/create', postVars,
		function(response) {
			if(response.error) {
				$("#goalkeepersaves").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#goalkeepersaves").after("<tr><td>Time Slot:</td><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td colspan=2>" + response.date + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // saveGoalkeeperSaves()

function deleteGoalkeeperSaves(id) {
	$.post('/services/eventgoalkeepersaves/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to delete penalty.");
			} else {
				$('#goal_object_'+id).remove();
			}
		}, "json"
	);
} // deleteGoalkeeperSaves()

