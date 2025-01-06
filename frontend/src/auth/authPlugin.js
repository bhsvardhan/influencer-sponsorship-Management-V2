export default {
  install(app) {
    app.config.globalProperties.$checkUserRole = function (roleString) {
      const role = localStorage.getItem("role");
      console.log(role);
      if (roleString == "admin" && role != 1) {
        this.$router.push("/error-page");
      } else if (roleString == "influencer" && role != 3) {
        this.$router.push("/error-page");
      } else if (roleString == "sponsor" && role != 2) {
        this.$router.push("/error-page");
      }
    };
  },
};
