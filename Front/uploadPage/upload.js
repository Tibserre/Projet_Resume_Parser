window.onload = function () {
    JSONResponse=getDataFromAPI();
    
};


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
        console.log(resultatJSON.reponse);
        return resultatJSON.reponse;
      })
  }


function parsingJSON(JSON){
console.log(JSON.Promise);
}