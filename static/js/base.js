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
	var postVars = $('#event_id, #goals :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventgoals/create', postVars,
		function(response) {
			if(response.error) {
				$("#goals").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#goals").after("<tr><td>" + response.team + "</td><td>" +
					response.player + "</td><td>" + response.period + 
					"</td><td colspan=2>" + response.time_minute + ":" + response.time_second + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // saveGoal()

function savePenalty() {
	var postVars = $('#penalties :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventpenalties/create', postVars,
		function(response) {
			if(response.error) {
				$("#create_form").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#create_form").after("<tr><td>Time Slot:</td><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td colspan=2>" + response.date + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // savePenalty()

function saveSuspension() {
	var postVars = $('#suspensions :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventsuspensions/create', postVars,
		function(response) {
			if(response.error) {
				$("#create_form").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#create_form").after("<tr><td>Time Slot:</td><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td colspan=2>" + response.date + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // saveSuspension()

function saveGoalkeeperSaves() {
	var postVars = $('#saves :input:not(:checkbox), #goals :input:checkbox:checked').serialize();
	$.post('/services/eventgoalkeepersaves/create', postVars,
		function(response) {
			if(response.error) {
				$("#create_form").after("<tr><td colspan=6>Error occured while saving goal: " + response.error + "</td></tr>");
			} else {
				$("#create_form").after("<tr><td>Time Slot:</td><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td colspan=2>" + response.date + "</td></tr>");
			}
		}, "json"
	);
	return false;
} // saveGoalkeeperSaves()

