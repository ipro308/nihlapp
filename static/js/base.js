// creates game event
function saveTimeSlot() {
	if($('#event_type').val() == 0) {
		alert("Please select game type.");
		return false;
	}		
	if($('#event_rink').val() == 0) {
		alert("Please select rink.");
		return false;
	}		
	if(!$('#event_date').val()) {
		alert("Please select date.");
		return false;
	}		
	var postVars = $('#create_event :input:not(:checkbox), #create_event :input:checkbox:checked').serialize();
	$.post('/services/events/create', postVars,
		function(response) {
			if(response.error) {
				$("#create_form").after("<tr><td colspan=6>Error occured while saving timeslot: " + response.error + "</td></tr>");
			} else {
				$("#create_form").after("<tr id='event_object_" + response.object_id + "'><td>" + response.eventType + "</td><td>" +
					response.rink + "</td><td>" + response.date + "</td><td>" + response.time + "</td>" +
					"<td><input type='button' name='edit_event' id='edit_event' value='Edit' onClick='editTimeSlot(" + response.object_id + ")'/> " +
					"<input type='button' name='delete_event' id='delete_event' value='Delete' onClick='deleteTimeSlot(" + response.object_id + ")'/></td></tr>");					
				$('#event_type').val(0);
				$('#event_rink').val(0);
				$('#event_date').val(null);
				$('#event_hour').val('01');
				$('#event_minute').val('00');
				$('#event_am').val('PM');
			}
		}, "json"
	);
	return false;
} // createTimeSlot()

// edits game event
function editTimeSlot(id) {
	$.post('/services/events/detail', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Unable to edit time slot: " + response.error);
			} else {
				$.post('/services/events/delete', {'object_id': id},
					function(responseDelete) {	
						if(responseDelete.error) {
							alert("Unable to edit time slot: " + responseDelete.error);
						} else {
							$('#event_object_'+id).remove();
							$('#event_type').val(response.type);
							$('#event_rink').val(response.rink);
							$('#event_date').val(response.date);
							$('#event_hour').val(response.hour);
							$('#event_minute').val(response.minute);
							$('#event_am').val(response.am);								
						}
					}, "json"
				);
			}
		}, "json"
	);
	return false;
} // editTimeSlot()

//deletes game event
function deleteTimeSlot(id) {
	$.post('/services/events/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Unable to delete time slot: " + response.error);
			} else {
				$('#event_object_'+id).remove();
			}
		}, "json"
	);
	return false;
} // deleteTimeSlot()

//saves a goal record
function saveGoal() {
	if($('#goal_team').val() == 0) {
		alert("Please select a team.");
		return false;
	}	
	if(!$('#goal_player').val()) {
		alert("Please provide goal player number.");
		return false;
	}
	if($('#goal_period').val() == 0) {
		alert("Please select a period.");
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
				$("#goals").after("<tr id='goal_object_" + response.object_id + "'><td>" + response.team + "</td><td>" +
					response.player + "</td><td>" + formatPeriod(response.period) + 
					"</td><td>" + response.time_minute + ":" + response.time_second + "</td>" +
					"<td><input type='button' name='edit_goal' id='edit_goal' value='Edit' onClick='editGoal(" + response.object_id + ")'/> " +
					"<input type='button' name='delete_goal' id='delete_goal' value='Delete' onClick='deleteGoal(" + response.object_id + ")'/></td></tr>");
				$('#goal_team').val(0);
				$('#goal_player').val(null);
				$('#goal_period').val(0);
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
	if($('#penalty_team').val() == 0) {
		alert("Please select a team.");
		return false;
	}	
	if(!$('#penalty_player').val()) {
		alert("Please provide goal player number.");
		return false;
	}
	if($('#penalty_period').val() == 0) {
		alert("Please select a period.");
		return false;
	}	
	if(!$('#penalty_time_minute').val()) {
		alert("Please provide penalty minute.");
		return false;
	}
	if(!$('#penalty_time_second').val()) {
		alert("Please provide penalty second.");
		return false;
	}	
	if($('#penalty_offense').val() == 0) {
		alert("Please select penalty offense.");
		return false;
	}	
	if(!$('#penalty_time_on_minute').val()) {
		alert("Please provide penalty time on minute.");
		return false;
	}
	if(!$('#penalty_time_on_second').val()) {
		alert("Please provide penalty time on second.");
		return false;
	}	
	if(!$('#penalty_time_off_minute').val()) {
		alert("Please provide penalty time off minute.");
		return false;
	}
	if(!$('#penalty_time_off_second').val()) {
		alert("Please provide penalty time off second.");
		return false;
	}	
	if(isNaN($('#penalty_player').val()) || $('#penalty_player').val() < 0 ) {
		alert("Invalid player number.");
		return false;
	}	
	if(isNaN($('#penalty_time_minute').val()) || $('#penalty_time_minute').val() < 0 || $('#penalty_time_minute').val() > 59 ) {
		alert("Invalid penalty minute.");
		return false;
	}		
	if(isNaN($('#penalty_time_second').val()) || $('#penalty_time_second').val() < 0 || $('#penalty_time_second').val() > 59 ) {
		alert("Invalid penalty second.");
		return false;
	}	
	if(isNaN($('#penalty_time_on_minute').val()) || $('#penalty_time_on_minute').val() < 0 || $('#penalty_time_on_minute').val() > 59 ) {
		alert("Invalid penalty time on minute.");
		return false;
	}		
	if(isNaN($('#penalty_time_on_second').val()) || $('#penalty_time_on_second').val() < 0 || $('#penalty_time_on_second').val() > 59 ) {
		alert("Invalid penalty time on second.");
		return false;
	}
	if(isNaN($('#penalty_time_off_minute').val()) || $('#penalty_time_off_minute').val() < 0 || $('#penalty_time_off_minute').val() > 59 ) {
		alert("Invalid penalty time off minute.");
		return false;
	}		
	if(isNaN($('#penalty_time_off_second').val()) || $('#penalty_time_off_second').val() < 0 || $('#penalty_time_off_second').val() > 59 ) {
		alert("Invalid penalty time off second.");
		return false;
	}	
	var postVars = $('#event_id, #penalties :input:not(:checkbox), #penalties :input:checkbox:checked').serialize();
	$.post('/services/eventpenalties/create', postVars,
		function(response) {
			if(response.error) {
				$("#penalties").after("<tr><td colspan=6>Error occured while saving penalty: " + response.error + "</td></tr>");
			} else {
				$("#penalties").after("<tr id='penalty_object_" + response.object_id + "'><td>" + response.team + "</td><td>" +
						response.player + "</td><td>" + formatPeriod(response.period) + 
						"</td><td>" + response.time_minute + ":" + response.time_second + "</td>" +
						"<td>" + response.offense + "</td>" +
						"<td>" + response.time_on_minute + ":" + response.time_on_second + "</td>" +
						"<td>" + response.time_off_minute + ":" + response.time_off_second + "</td>" +
						"<td><input type='button' name='edit_penalty' id='edit_penalty' value='Edit' onClick='editPenalty(" + response.object_id + ")'/> " +
						"<input type='button' name='delete_penalty' id='delete_penalty' value='Delete' onClick='deletePenalty(" + response.object_id + ")'/></td></tr>");
				$('#penalty_team').val(0);
				$('#penalty_player').val(null);
				$('#penalty_period').val(0);
				$('#penalty_offense').val(0);
				$('#penalty_time_minute').val(null);
				$('#penalty_time_second').val(null);
				$('#penalty_time_on_minute').val(null);
				$('#penalty_time_on_second').val(null);
				$('#penalty_time_off_minute').val(null);
				$('#penalty_time_off_second').val(null);
			}
		}, "json"
	);
	return false;
} // savePenalty()

function editPenalty(id) {
	$.post('/services/eventpenalties/detail', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to edit penalty.");
			} else {
				deletePenalty(id);
				$('#penalty_team').val(response.team);
				$('#penalty_player').val(response.player);
				$('#penalty_period').val(response.period);
				$('#penalty_offense').val(response.offense);
				$('#penalty_time_minute').val(response.time_minute);
				$('#penalty_time_second').val(response.time_second);
				$('#penalty_time_on_minute').val(response.time_on_minute);
				$('#penalty_time_on_second').val(response.time_on_second);
				$('#penalty_time_off_minute').val(response.time_off_minute);
				$('#penalty_time_off_second').val(response.time_off_second);				
			}
		}, "json"
	);
	return false;
} // editGoal()

function deletePenalty(id) {
	$.post('/services/eventpenalties/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to delete penalty.");
			} else {
				$('#penalty_object_'+id).remove();
			}
		}, "json"
	);
} // deletePenalty()

function saveSuspension() {
	if($('#suspension_team').val() == 0) {
		alert("Please select a team.");
		return false;
	}	
	if(!$('#suspension_player').val()) {
		alert("Please provide player number.");
		return false;
	}
	if($('#suspension_player_lastname').val() == "") {
		alert("Please provide player's last name.");
		return false;
	}		
	if(isNaN($('#suspension_player').val()) || $('#suspension_player').val() < 0 ) {
		alert("Invalid player number.");
		return false;
	}		
	var postVars = $('#event_id, #suspensions :input:not(:checkbox), #suspensions :input:checkbox:checked').serialize();
	$.post('/services/eventsuspensions/create', postVars,
		function(response) {
			if(response.error) {
				$("#suspensions").after("<tr><td colspan=6>Error occured while saving suspension: " + response.error + "</td></tr>");
			} else {
				$("#suspensions").after("<tr id='suspension_object_" + response.object_id + "'><td>" + response.team + "</td><td>" +
						response.player + "</td><td>" + response.player_last_name + 
						"<td><input type='button' name='edit_goal' id='edit_goal' value='Edit' onClick='editSuspension(" + response.object_id + ")'/> " +
						"<input type='button' name='delete_suspension' id='delete_suspension' value='Delete' onClick='deleteSuspension(" + response.object_id + ")'/></td></tr>");
				$('#suspension_team').val(0);
				$('#suspension_player').val(null);
				$('#suspension_player_lastname').val(null);
			}
		}, "json"
	);
	return false;
} // saveSuspension()

function editSuspension(id) {
	$.post('/services/eventsuspensions/detail', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to edit suspension.");
			} else {
				deleteSuspension(id);
				$('#suspension_team').val(response.team);
				$('#suspension_player').val(response.player);
				$('#suspension_player_lastname').val(response.player_last_name);
			}
		}, "json"
	);
	return false;
} // editSuspension()

function deleteSuspension(id) {
	$.post('/services/eventsuspensions/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to delete suspension.");
			} else {
				$('#suspension_object_'+id).remove();
			}
		}, "json"
	);
} // deleteSuspension()

function saveGoalkeeperSaves() {
	if($('#saves_team').val() == 0) {
		alert("Please select a team.");
		return false;
	}	
	if(!$('#saves_player').val()) {
		alert("Please provide player number.");
		return false;
	}		
	if(isNaN($('#saves_player').val()) || $('#saves_player').val() < 0 ) {
		alert("Invalid player number.");
		return false;
	}	
	if(!($('#saves_1st').val()) || isNaN($('#saves_1st').val()) || $('#saves_1st').val() < 0 ) {
		alert("Please provide a valid number for 1st period saves.");
		return false;
	}
	if(!($('#saves_2nd').val()) || isNaN($('#saves_2nd').val()) || $('#saves_2nd').val() < 0 ) {
		alert("Please provide a valid number for 2nd period saves.");
		return false;
	}
	if(!($('#saves_3rd').val()) || isNaN($('#saves_3rd').val()) || $('#saves_3rd').val() < 0 ) {
		alert("Please provide a valid number for 3rd period saves.");
		return false;
	}
	if(!($('#saves_ot').val()) || isNaN($('#saves_ot').val()) || $('#saves_ot').val() < 0 ) {
		alert("Please provide a valid number for overtime saves.");
		return false;
	}	
	var postVars = $('#event_id, #saves :input:not(:checkbox), #saves :input:checkbox:checked').serialize();
	$.post('/services/eventgoalkeepersaves/create', postVars,
		function(response) {
			if(response.error) {
				$("#saves").after("<tr><td colspan=6>Error occured while saving goalkeeper: " + response.error + "</td></tr>");
			} else {
				$("#saves").after("<tr id='saves_object_" + response.object_id + "'><td>" + response.team + "</td><td>" + 
						response.player + "</td><td>" + response.first + "</td><td>" + response.second + "</td><td>" + response.third + "</td><td>" + response.ot + "</td>" +
						"<td><input type='button' name='edit_saves' id='edit_saves' value='Edit' onClick='editGoalkeeperSaves(" + response.object_id + ")'/> " +
						"<input type='button' name='delete_saves' id='delete_saves' value='Delete' onClick='deleteGoalkeeperSaves(" + response.object_id + ")'/></td></tr>");
				$('#saves_team').val(0);
				$('#saves_player').val(null);
				$('#saves_1st').val(null);
				$('#saves_2nd').val(null);
				$('#saves_3rd').val(null);
				$('#saves_ot').val(null);
			}
		}, "json"
	);
	return false;
} // saveGoalkeeperSaves()

function editGoalkeeperSaves(id) {
	$.post('/services/eventgoalkeepersaves/detail', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to edit goalkeeper.");
			} else {
				deleteGoalkeeperSaves(id);
				$('#saves_team').val(response.team);
				$('#saves_player').val(response.player);
				$('#saves_1st').val(response.first);
				$('#saves_2nd').val(response.second);
				$('#saves_3rd').val(response.third);
				$('#saves_ot').val(response.ot);
			}
		}, "json"
	);
	return false;
} // editGoalkeeperSaves()

function deleteGoalkeeperSaves(id) {
	$.post('/services/eventgoalkeepersaves/delete', {'object_id': id},
		function(response) {	
			if(response.error) {
				alert("Error: unable to delete goalkeeper saves.");
			} else {
				$('#saves_object_'+id).remove();
			}
		}, "json"
	);
} // deleteGoalkeeperSaves()

// formats saved period # to human readable text
function formatPeriod(input) {
	var result = null;
	switch(input) {
		case "1":
			result = "1st Period";
			break;
		case "2":
			result = "2nd Period";
			break;
		case "3":
			result = "3rd Period";
			break;
		case "4":
			result = "Overtime";
			break;
		default:
			result = null;
	}
	return result;
}

function requestDateTime(id) {
	$.post('/services/scheduling/schedule', {'matchup_id': id, 'event_id': $('#matchup_select_'+id).val()},
			function(response) {	
				if(response.error) {
					alert("Error: " + response.error);
				} else {
					$('#matchup_td_'+id).html(response.status);
				}
			}, "json"
		);
}

function requestReject(matchupid, eventid) {
	$.post('/services/scheduling/reject', {'matchup_id': matchupid, 'event_id': eventid},
			function(response) {	
				if(response.error) {
					alert("Error: " + response.error);
				} else {
					$('#matchup_td_'+matchupid).html(response.status);
				}
			}, "json"
		);
}

function requestConfirm(matchupid, eventid) {
	$.post('/services/scheduling/confirm', {'matchup_id': matchupid, 'event_id': eventid},
			function(response) {	
				if(response.error) {
					alert("Error: " + response.error);
				} else {
					$('#matchup_td_'+matchupid).html(response.status);
				}
			}, "json"
		);
}

// initialize everything
var init = function() {
	
	// information tooltip will appear on objects with title parameter.
    $('[title]').tooltip({
        track: true,
        delay: 50,
        showURL: false,
        showBody: " - ",
        opacity: 0.85,
        extraClass: "tooltip",
    });
 
}
 
$(document).ready(init);
