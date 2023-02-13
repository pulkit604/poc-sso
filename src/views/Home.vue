<template>
  <div class="home">
    <h4>Hello, Welcome to this Proof-of-concept for testing Pulkit's SSO!</h4>
    <a
      :href="
        authUri +
          '?response_type=code&clientId=' +
          clientId +
          '&clientSecret=' +
          clientSecret +
          '&redirectUri=' +
          redirectUri +
          '&state=123yss'
      "
    ><button>Login using Pulkit's SSO</button></a>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "Home",
  components: {
  },
  data() {
    return {
      clientId: "Puoilj5i45",
      clientSecret: "pouih4565h",
      redirectUri: "http://localhost:8080/success",
      authUri: "http://127.0.0.1:5000/auth",
      scopes: []
    }
  }
};
</script>
