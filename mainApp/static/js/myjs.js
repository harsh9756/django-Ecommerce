var counter = 0;
document.getElementById('counter').value=counter;
function delbtn(id) {
  event.preventDefault();
  var x = document.getElementsByName('propkey' + id)
  var y = document.getElementsByName('propvalue' + id)
  document.getElementById(id).remove()
  x[0].remove();
  y[0].remove();
}

function addnewbtn(event) {
  event.preventDefault();
  var output = document.getElementById("inptContainer")
  var divv= document.createElement("div")
  counter = counter + 1;
  document.getElementById('counter').value=counter;
  var input1 = document.createElement('input');
  input1.type = 'text';
  input1.style.marginBottom = '4px';
  input1.placeholder = 'Enter Property';
  input1.className = "form-control w-30"
  input1.name = "propkey" + counter
  
  var input2 = document.createElement("input");
  input2.type = 'text';
  input2.style.marginBottom = '4px';
  input2.style.marginLeft = '4px';
  input2.placeholder = 'Enter Value';
  input2.className = "form-control w-30"
  input2.name = "propvalue" + counter
  
  var del = document.createElement('button');
  del.innerHTML = 'X';
  del.className = 'btn btn-danger mx-1'
  del.id = counter
  del.onclick = function () {
    delbtn(this.id);
  }
  output.appendChild(divv)  
  divv.appendChild(input1)  
  divv.appendChild(input2)  
  divv.appendChild(del)  
}
function deleteproper(button){
  event.preventDefault();
  var row = button.parentNode;
  row.remove();
}

function update_btn(){
  const mainCont=document.getElementById("inptContainer")
  var len = mainCont.children.length
  var dict={}
  for (let i=0; i<len;i++){
    var key=mainCont.children[i].children[0].value
    var value= mainCont.children[i].children[1].value
    dict[key]=value
  }
  document.getElementById('jsdata').value=JSON.stringify(dict);
}