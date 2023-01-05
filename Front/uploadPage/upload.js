window.onload = function () {
    JSONResponse=getDataFromAPI();
    
};

function getResult(){
    console.log("inside getResult");
    fetch("http://127.0.0.1:2000/resume-parser")
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
    
}

function getDataFromAPI() {
    return fetch('http://127.0.0.1:2000/resume-parser', {
        method: 'GET',
      })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        var resultat = JSON.stringify(data);
        var resultatJSON = JSON.parse(resultat)
        console.log(resultatJSON);
        return resultatJSON;
      })
  }


function parsingJSON(JSON){
console.log(JSON.Promise);
}