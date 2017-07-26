(function () {
	// Initialize Firebase
  var config = {
    apiKey: "AIzaSyDVvWK2oZmqNnsNpZ_OGOoRkDi6gKPu88Y",
    authDomain: "fanapton.firebaseapp.com",
    databaseURL: "https://fanapton.firebaseio.com",
    projectId: "fanapton",
    storageBucket: "fanapton.appspot.com",
    messagingSenderId: "872155897203"
  };

  firebase.initializeApp(config);

	firebase.auth().currentUser.getToken(/* forceRefresh */ true).then(function(idToken) {
    // Send token to your backend via HTTPS
    // ...
  }).catch(function(error) {
    // Handle error
  }); 

}());