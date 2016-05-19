$("#addrunbtn").click(function () {
	addRun();
});

function addRun() {
	var runlist = $("#runlist");
	var runnum = (runlist.children().length / 2) + 1;
	runlist.append('<li class="btn btn-default run" data-toggle="collapse" data-target="#run_detail' + runnum + '">Run ' + runnum + '</li>');
	runlist.append('<div id="run_detail' + runnum + '" class="collapse">'
		+ '<div class="form-group"><label>Run number</label><input type="text" class="form-control" id="runnum" name="runnum"></input></div>'
		+ '<div class="form-group"><label>Number of TRs</label><input type="text" class="form-control" id="trnum" name="trnum"></input></div>'
		+ '<div class="form-group"><label>Sequence</label><input type="text" class="form-control" id="sequence" name="sequence"></input></div>'
		+ '<div class="form-group"><label>Stimuli</label><input type="text" class="form-control" id="stimuli" name="stimuli"></input></div>'
		+ '<div class="form-group"><label>Run notes</label><input type="text" class="form-control" id="runnotes" name="runnotes"></input></div>'
		+ '</div>');
	
}

$('#close_copyoutput').click(function () {
    $('#copyoutput').removeClass('active')
});

$('#exportbtn').click(function() {
  event.preventDefault();
  var data = new FormData($('#scanform')[0]);
  $.ajax({
        type: 'POST',
        url: '/export',
        data: data,
        contentType: false,
        processData: false,
        dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
    	console.log(data);
        $('#copyoutput').addClass('active');
        var output = document.getElementById('outputtext');
        output.innerText = data['text'];
        document.getElementById('copyjson').removeAttribute('disabled');
    }).fail(function(data){
        $('#error').show();
    });
});

$('#copydata').click(function() {
  var copyTextarea = document.getElementById('outputtext');
  copyTextarea.select();
  try {
    var successful = document.execCommand('copy');
    $('#copyoutput').removeClass('active');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Copying text command was ' + msg);
  } catch (err) {
    console.log('Oops, unable to copy');
  }
});