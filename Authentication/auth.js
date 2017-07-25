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

  //Add logout evet
  btnLogout.addEventListener('click', e => {
    firebase.auth().signOut();
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

