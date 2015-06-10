function populate_alerts() {
  var row_elem = document.createElement("div");
  row_elem.className = "row";

  var number_of_columns = 3;

  var column_elem_list = [];
  for (var i=0; i<number_of_columns; i++) {
    column_elem_list[i] = document.createElement("div");
    column_elem_list[i].className = "col-md-4 col-sm-6";
  }

  var panel_html_array = [];
  // create an DOM object or something of each string from this
  // array and append to each column_elem instance.

  $.ajax({
    url:"../get_triggered_reminders/",
    dataType:"html",
    async:false,
    success:function(data) {
      panel_html_array = data.split("monitor_tag_split_here");
    }
  });

  for (var i=0; i<panel_html_array.length; i++) {
    var existing_html = column_elem_list[i%number_of_columns].innerHTML;
    column_elem_list[i%number_of_columns].innerHTML = existing_html + panel_html_array[i];
  }

  for(var i=0; i<number_of_columns; i++)
    row_elem.appendChild(column_elem_list[i]);

  document.getElementsByClassName("container")[0].appendChild(row_elem);
}
