function insert_reminder_body_initialize() {
  var attribs = [
    document.getElementById("id_attribute1"),
    document.getElementById("id_attribute2")
  ];
  for(var i=0; i<attribs.length; i++)
    attribs[i].onchange=get_trigger_form;
}

var walk_the_DOM = function walk(node, func) {
  func(node);
  node = node.firstChild;
  while(node) {
    walk(node, func);
    node = node.nextSibling;
  }
}

function add_trigger_field() {
  trigger_count  += 1;

  var trigger1  = document.getElementById("id_attribute1");
  var trigger1_h= document.getElementById("id_attribute1_hidden");
  var tbody     = trigger1.parentNode;
  while(tbody.tagName.toLowerCase() != "tbody")
    tbody = tbody.parentNode;

  var new_tr  = document.createElement("tr");
  var new_th  = document.createElement("th");
  var new_td  = document.createElement("td");

  var new_trigger   = trigger1.cloneNode(true);
  new_trigger.id    = "id_attribute"+trigger_count;
  new_trigger.name  = "attribute"+trigger_count;
  new_trigger.onchange  = get_trigger_form;

  var new_trigger_hidden  = trigger1_h.cloneNode(true);
  new_trigger_hidden.id   = new_trigger.id+"_hidden";
  new_trigger_hidden.type = "hidden";
  new_trigger_hidden.name = new_trigger.name+"_hidden";

  new_td.appendChild(new_trigger);
  new_td.appendChild(new_trigger_hidden);

  var new_label = document.createElement("label");
  new_label.for = new_trigger.id;
  new_label.textContent = "Attribute"+trigger_count;
  new_th.appendChild(new_label);

  tbody.appendChild(new_tr);
  new_tr.appendChild(new_th);
  new_tr.appendChild(new_td);
  // instead of the above, try to find the common
  // parent of two already inserted attribute fields
  // and duplicate them;
}

function get_trigger_form() {
  var pp  = this.parentNode.parentNode;
  var t   = this;
  var option = this.options[this.selectedIndex].textContent;
  $.ajax({
    url:"../get_attrib_form?attrib="+option,
    dataType:"html",
    async:false,
    success:function(data) {
      var name = t.id+"_attrib_form";
      var existing_form = document.getElementById(name);

      if(existing_form != null) {
        existing_form.remove();
        // clear the fields of existing_form's mom ?
      }

      var attrib_form       = document.createElement("td");
      attrib_form.innerHTML = data;

      walk_the_DOM(
          attrib_form,
          function (node) {
            node.id   = name+node.id;
            node.mom  = t.id;
          }
          );

      attrib_form.id        = name;
      pp.appendChild(attrib_form);
    }
  });

  // find parent 'form' tag
  var parent_form = this.parentNode;
  while (parent_form.tagName.toLowerCase() != 'form')
    parent_form = parent_form.parentNode;

  parent_form.onsubmit = some_function;
  if (typeof(parent_form.triggers) == "undefined")
    parent_form.triggers= [];
  parent_form.triggers.push(this.id);
}

function make_attribute_string(t, field) {
  var mom = document.getElementById(t.mom);

  if(typeof(mom.attrib_fields) == "undefined") {
    mom.attrib_fields = {};
  }
  mom.attrib_fields[field] = 1;
  mom[field] = t.value;
}

function some_function() {
  for (var idx = 0; idx < this.triggers.length; idx++) {
    // this.triggers contains a list of ids that refer to
    // moms in make_attribute_string; change the value field
    // of these moms
    var mom = document.getElementById(this.triggers[idx]);
    var mom_hidden = document.getElementById(mom.id+"_hidden");
    mom.temp_dict = {};
    for (var key in mom.attrib_fields) {
      if (key != undefined)
        mom.temp_dict[key] = mom[key];
    }
    mom_hidden.setAttribute("value", JSON.stringify(mom.temp_dict));
  }
}
