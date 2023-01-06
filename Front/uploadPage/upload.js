window.onload = function () {
  JSONResponse = getDataFromAPI();
  console.log(JSONResponse);
};


function getDataFromAPI() {
  return fetch('http://127.0.0.1:2000/resume-parser', {
    method: 'GET',
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      var resultat = JSON.stringify(data);
      var resultatJSON = JSON.parse(resultat)
      console.log(JSON.stringify(resultatJSON.reponse));
      ajoutJson(resultatJSON.reponse)
      return resultatJSON;
    })
}


function parsingJSON(JSON) {
  console.log(JSON.Promise);
}





// fonction pour afficher les données d'un objet ou d'un tableau
function displayData(data) {
  // création de la structure HTML de base
  const container = document.createElement('div');

  // si l'objet est un tableau, on le parcourt et on affiche chaque élément
  if (Array.isArray(data)) {
    for (const element of data) {
      container.appendChild(displayData(element));
    }
  }
  // si l'objet est un objet, on parcourt ses propriétés et on les affiche
  else if (typeof data === 'object') {
    for (const key in data) {
      // création de l'élément HTML pour la propriété
      const property = document.createElement('div');
      property.innerHTML = `<h3>${key}</h3>`;

      // ajout de la valeur de la propriété à l'élément
      property.appendChild(displayData(data[key]));

      // ajout de la propriété à la structure HTML
      container.appendChild(property);
    }
  }
  // si l'objet est une chaîne de caractères, on l'affiche
  else {
    const element = document.createElement('p');
    element.innerText = data;
    container.appendChild(element);
  }

  // retour de la structure HTML
  return container;
}

function ajoutJson(data) {
  const jsonContainer = document.getElementById('json');

  // ajout du JSON à l'élément
  jsonContainer.appendChild(displayData(data));
}
