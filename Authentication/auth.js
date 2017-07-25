(function() {

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

  //Get elements
  const txtEmail = document.getElementById('txtEmail'); 
  const txtPassword = document.getElementById('txtPassword');
  const btnLogin = document.getElementById('btnLogin');
  const btnSignup = document.getElementById('btnSignup');
  const btnLogout = document.getElementById('btnLogout');
  const btnGoogleSignin = document.getElementById('btnGoogleSignin');
  const btnFBSignin = document.getElementById('btnFBSignin');

  //Add login event
  btnLogin.addEventListener('click', e => {
    //get email and password
    const email = txtEmail.value;
    const pass = txtPassword.value;
    const auth = firebase.auth();
    //sign in
    const promise = auth.signInWithEmailAndPassword(email, pass);
    promise.catch(e => console.log(e.message));
  });

  //Add signup event
  btnSignup.addEventListener('click', e => {
    //get email and password
    //TODO: check for real email    
    const email = txtEmail.value;
    const pass = txtPassword.value;
    const auth = firebase.auth();
    //sign up
    const promise = auth.createUserWithEmailAndPassword(email, pass);
    promise.catch(e => console.log(e.message));
  });

  //Add logout event
  btnLogout.addEventListener('click', e => {
    firebase.auth().signOut();
  });

  //Add signin with google event
  btnGoogleSignin.addEventListener('click', e => {
    var provider = new firebase.auth.GoogleAuthProvider();
    firebase.auth().signInWithRedirect(provider);
  });

  //Add signin with facebook event
  btnFBSignin.addEventListener('click', e => {
    var provider = new firebase.auth.FacebookAuthProvider();
    firebase.auth().signInWithRedirect(provider);
  });

  //Get Google provider's OAuth token 
  firebase.auth().getRedirectResult().then(function(result) {
    if (result.credential) {
      // This gives you a Google Access Token. You can use it to access the Google API.
      var token = result.credential.accessToken;
    }
    // The signed-in user info.
    var user = result.user;
  }).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;
    // The email of the user's account used.
    var email = error.email;
    // The firebase.auth.AuthCredential type that was used.
    var credential = error.credential;
    // ...
  });

  //Add realtime listener
  firebase.auth().onAuthStateChanged(firebaseUser => {
    if(firebaseUser) {
      console.log(firebaseUser);
      btnLogout.removeAttribute('hidden');
    }
    else {
      console.log('not log in');
    }
  });

}());

