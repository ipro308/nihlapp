// creates game event
function createTimeSlot(e) {
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
function editTimeSlot(e) {
	alert("Not implemented yet");
	return false;
} // editTimeSlot()
